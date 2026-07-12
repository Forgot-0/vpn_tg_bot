from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.commands.subscriptions.create_subscription import ConfiguratePlanDTO
from app.application.dtos.subscriptions import RenewSubscriptionResult
from app.application.dtos.users import UserJWTData
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.entities.order import Order
from app.domain.entities.payment import Payment
from app.domain.entities.plan import SubscriptionPlan
from app.domain.entities.subscription import Subscription
from app.domain.errors import (
    PlanNotFoundError,
    SubscriptionNotFoundError,
    SubscriptionNotRenewableError,
)
from app.domain.repositories.orders import OrderRepository
from app.domain.repositories.payments import PaymentRepository
from app.domain.repositories.plans import PlanRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.values.order import OrderStatus, OrderType
from app.domain.values.payments import PaymentProvider
from app.domain.values.subscriptions import (
    RenewalMode,
    SubscriptionLimits,
    SubscriptionStatus,
)


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RenewSubscriptionCommand(BaseCommand):
    user_jwt_data: UserJWTData
    subscription_id: UUID
    renewal_mode: RenewalMode
    idempotency_key: str
    return_url: str
    currency: str = "RUB"
    plan_draft: ConfiguratePlanDTO | None = None


@dataclass(frozen=True)
class RenewSubscriptionCommandHandler(
    BaseCommandHandler[RenewSubscriptionCommand, RenewSubscriptionResult]
):
    plan_repository: PlanRepository
    subscription_repository: SubscriptionRepository
    order_repository: OrderRepository
    payment_repository: PaymentRepository
    payment_gateway: PaymentGateway
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: RenewSubscriptionCommand) -> RenewSubscriptionResult:
        subscription = await self.subscription_repository.get_by_id(command.subscription_id)
        if subscription is None:
            raise SubscriptionNotFoundError(entity_id=str(command.subscription_id))

        if subscription.user_id != command.user_jwt_data.id:
            raise SubscriptionNotFoundError(entity_id=str(command.subscription_id))

        if subscription.status not in {
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.EXPIRED,
            SubscriptionStatus.SUSPENDED,
        }:
            raise SubscriptionNotRenewableError(status_value=subscription.status.value)

        plan = await self.plan_repository.get_by_id(subscription.plan_id)
        if plan is None:
            raise PlanNotFoundError(entity_id=str(subscription.plan_id))

        plan.ensure_active()
        new_limit = self._resolve_renewal_limits(subscription, command)
        price = self._calculate_price(plan, new_limit, command.currency)

        order = Order(
            user_id=command.user_jwt_data.id,
            subscription_id=subscription.id,
            amount=price,
            type=OrderType.RENEW_SUBSCRIPTION,
            status=OrderStatus.WAITING_PAYMENT,
            subscription_limit=new_limit,
            renewal_mode=command.renewal_mode,
        )
        await self.order_repository.add(order)

        payment = Payment(
            order_id=order.id,
            amount=price,
            provider=PaymentProvider.YOOKASSA,
            idempotency_key=command.idempotency_key,
        )
        await self.payment_repository.add(payment)
        await self.uow.commit()

        gateway_result = await self.payment_gateway.create_payment(payment, return_url=command.return_url)

        payment.awaiting_confirmation(
            external_id=gateway_result.external_id,
            confirmation_url=gateway_result.confirmation_url or "",
        )
        await self.payment_repository.update(payment)
        await self.uow.commit()

        logger.info(
            "Subscription renewal initiated",
            extra={
                "user_id": str(command.user_jwt_data.id),
                "subscription_id": str(subscription.id),
                "order_id": str(order.id),
                "renewal_mode": command.renewal_mode.value,
            },
        )

        return RenewSubscriptionResult(
            subscription_id=subscription.id,
            order_id=order.id,
            payment_id=payment.id,
            confirmation_url=payment.confirmation_url or "",
        )

    def _resolve_renewal_limits(
        self,
        subscription: Subscription,
        command: RenewSubscriptionCommand,
    ) -> SubscriptionLimits:
        if command.plan_draft is not None:
            return SubscriptionLimits.create(
                duration_days=command.plan_draft.duration_days,
                trafic_bytes_limit=command.plan_draft.trafic_bytes_limit,
                max_devices=command.plan_draft.max_devices,
                features=command.plan_draft.features,
                protocols=command.plan_draft.protocols,
                strategy=command.plan_draft.strategy,
                reset_every_n_days=command.plan_draft.reset_every_n_days,
                custom_cron=command.plan_draft.custom_cron,
            )

        return subscription.limit

    def _calculate_price(self, plan: SubscriptionPlan, new_limit: SubscriptionLimits, currency: str):
        if plan.is_fixed:
            price = plan.fixed_price_for(currency)

            if price is None:
                raise PlanNotFoundError(entity_id=str(plan.id))

            return price

        plan.validate_draft(new_limit)

        return plan.calculate_price(new_limit)
