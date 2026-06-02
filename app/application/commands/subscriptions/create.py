from dataclasses import dataclass
from decimal import Decimal
import logging
from uuid import UUID, uuid4

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import CreateSubscriptionResultDTO
from app.application.dtos.users import UserJWTData
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.entities.payment import PaymentOrder
from app.domain.entities.subscription_draft import SubscriptionDraft
from app.domain.repositories.payments import PaymentOrderRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscription_drafts import SubscriptionDraftRepository
from app.domain.repositories.subscriptions import SubscriptionPlanRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.pricings import PricingService
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import PlanType, SubscriptionSpec


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    user_jwt_data: UserJWTData

    plan_id: UUID
    return_url: str

    duration_days: int | None = None
    traffic_limit_gb: Decimal | None = None
    max_devices: int = 1
    protocol_codes: frozenset[str] = frozenset()
    feature_codes: frozenset[str] = frozenset()


@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, CreateSubscriptionResultDTO]):
    plan_repository: SubscriptionPlanRepository
    draft_repository: SubscriptionDraftRepository
    server_repository: VPNServerRepository
    payment_repository: PaymentOrderRepository
    payment_gateway: PaymentGateway
    pricing_service: PricingService
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: CreateSubscriptionCommand) -> CreateSubscriptionResultDTO:
        plan = await self.plan_repository.get_by_id(command.plan_id)
        if plan is None or not plan.is_active:
            raise 

        if plan.plan_type == PlanType.FIXED:
            spec = plan.get_fixed_spec()
            price = plan.get_fixed_price()
        else:
            protocols = frozenset(ProtocolCode(p) for p in command.protocol_codes) or plan.get_allowed_protocols()
            features = frozenset(FeatureCode(f) for f in command.feature_codes)

            spec = SubscriptionSpec(
                protocols=protocols,
                duration_days=command.duration_days,
                traffic_limit_gb=command.traffic_limit_gb,
                max_devices=command.max_devices,
                features=features,
            )
            plan.validate_spec(spec)

            assert plan.pricing_rules is not None
            price = self.pricing_service.calculate(spec, plan.pricing_rules)

        server = await self.server_repository.get_max_free_server(spec.protocols, spec.features)
        if server is None:
            raise

        draft = SubscriptionDraft(
            id=uuid4(),
            user_id=command.user_jwt_data.id,
            plan_id=command.plan_id,
            server_id=server.id,
            spec=spec,
        )
        draft.recalculate_price(plan, self.pricing_service)
        draft.mark_ready_for_checkout()

        payment_order = PaymentOrder(
            id=uuid4(),
            draft_id=draft.id,
            user_id=command.user_jwt_data.id,
            amount=price,
            provider=self.payment_gateway.provider,
        )

        try:
            gateway_result = await self.payment_gateway.create_payment(
                payment_order,
                return_url=command.return_url,
            )
        except Exception:
            await self.uow.rollback()
            raise

        payment_order.awaiting_confirmation(
            external_id=gateway_result.external_id,
            confirmation_url=gateway_result.confirmation_url or "",
        )
        await self.draft_repository.add(draft)
        await self.payment_repository.add(payment_order)
        await self.uow.commit()

        await self.event_bus.publish(draft.pull_events())
        await self.event_bus.publish(payment_order.pull_events())

        return CreateSubscriptionResultDTO(
            draft_id=draft.id,
            payment_order_id=payment_order.id,
            confirmation_url=gateway_result.confirmation_url or "",
            amount=price.amount,
            currency=price.currency,
        )
