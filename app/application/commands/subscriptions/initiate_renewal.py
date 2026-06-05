from dataclasses import dataclass
import logging
from uuid import UUID, uuid4

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import CreateSubscriptionResultDTO
from app.application.dtos.users import UserJWTData
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.entities.checkout import CheckoutSession
from app.domain.entities.payment import PaymentIntent
from app.domain.errors import (
    PlanNotFoundError,
    SubscriptionNotFoundError,
    SubscriptionNotRenewableError,
)
from app.domain.repositories.checkouts import CheckoutSessionRepository
from app.domain.repositories.payments import PaymentIntentRepository
from app.domain.repositories.plans import PlanRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.pricings import PricingService
from app.domain.values.checkouts import CheckoutIntent
from app.domain.values.subscriptions import PlanConfiguration, SubscriptionStatus


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InitiateSubscriptionRenewalCommand(BaseCommand):
    user_jwt_data: UserJWTData
    subscription_id: UUID
    return_url: str
    duration_days: int | None = None


@dataclass(frozen=True)
class InitiateSubscriptionRenewalHandler(
    BaseCommandHandler[InitiateSubscriptionRenewalCommand, CreateSubscriptionResultDTO]
):
    subscription_repository: SubscriptionRepository
    plan_repository: PlanRepository
    checkout_repository: CheckoutSessionRepository
    payment_repository: PaymentIntentRepository
    payment_gateway: PaymentGateway
    pricing_service: PricingService
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: InitiateSubscriptionRenewalCommand) -> CreateSubscriptionResultDTO:
        subscription = await self.subscription_repository.get_by_id(command.subscription_id)
        if subscription is None or subscription.user_id != command.user_jwt_data.id:
            raise SubscriptionNotFoundError(entity_id=str(command.subscription_id))

        if subscription.status not in {
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.EXPIRED,
        }:
            raise

        if subscription.spec.is_time_limited is False:
            raise SubscriptionNotRenewableError(
                reason="Only time-limited subscriptions can be renewed",
            )

        if subscription.server_id is None:
            raise SubscriptionNotRenewableError(
                reason="Subscription has no associated server",
            )


        plan = await self.plan_repository.get_by_id(subscription.plan_id)
        if plan is None:
            raise PlanNotFoundError(entity_id=str(subscription.plan_id))

        if not plan.is_active:
            raise

        spec = subscription.spec
        if command.duration_days is not None:
            spec = PlanConfiguration(
                protocols=spec.protocols,
                duration_days=command.duration_days,
                traffic_limit_gb=spec.traffic_limit_gb,
                max_devices=spec.max_devices,
                features=spec.features,
                location_ids=spec.location_ids,
                server_group_ids=spec.server_group_ids,
            )
            plan.validate_spec(spec)

        if plan.is_fixed:
            price = plan.get_fixed_price()
        else:
            assert plan.pricing_rules is not None
            price = self.pricing_service.calculate(spec, plan.pricing_rules)

        checkout = CheckoutSession(
            id=uuid4(),
            user_id=command.user_jwt_data.id,
            plan_id=subscription.plan_id,
            server_id=subscription.server_id,
            spec=spec,
            metadata={
                "intent": CheckoutIntent.RENEWAL.value,
                "subscription_id": str(subscription.id),
            },
        )
        checkout.recalculate_price(plan, self.pricing_service)
        checkout.mark_ready_for_checkout()

        payment_intent = PaymentIntent(
            id=uuid4(),
            checkout_session_id=checkout.id,
            user_id=command.user_jwt_data.id,
            amount=price,
            provider=self.payment_gateway.provider,
        )

        try:
            gateway_result = await self.payment_gateway.create_payment(
                payment_intent,
                return_url=command.return_url,
            )
        except Exception:
            await self.uow.rollback()
            raise

        payment_intent.awaiting_confirmation(
            external_id=gateway_result.external_id,
            confirmation_url=gateway_result.confirmation_url or "",
        )
        await self.checkout_repository.add(checkout)
        await self.payment_repository.add(payment_intent)
        await self.uow.commit()

        await self.event_bus.publish(checkout.pull_events())
        await self.event_bus.publish(payment_intent.pull_events())

        return CreateSubscriptionResultDTO(
            checkout_session_id=checkout.id,
            payment_intent_id=payment_intent.id,
            confirmation_url=gateway_result.confirmation_url or "",
            amount=price.amount,
            currency=price.currency,
        )
