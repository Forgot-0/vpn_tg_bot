from __future__ import annotations

import logging
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import CreateSubscriptionResult
from app.application.dtos.users import UserJWTData
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.entities.order import Order
from app.domain.entities.payment import Payment
from app.domain.entities.subscription import Subscription
from app.domain.errors import PlanNotFoundError, UserNotFoundError
from app.domain.repositories.orders import OrderRepository
from app.domain.repositories.payments import PaymentRepository
from app.domain.repositories.plans import PlanRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.repositories.users import UserRepository
from app.domain.values.order import OrderStatus, OrderType
from app.domain.values.payments import PaymentProvider
from app.domain.values.subscriptions import SubscriptionLimits


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConfiguratePlanDTO:
    duration_days: int | None
    trafic_bytes_limit: int
    max_devices: int | None

    features: set[str]
    protocols: set[str]

    strategy: str
    reset_every_n_days: int | None = None
    custom_cron: str | None = None


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    user_jwt_data: UserJWTData
    plan_id: UUID
    idempotency_key: str

    return_url: str
    currency: str = "RUB"

    plan_draft: ConfiguratePlanDTO | None = None



@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, CreateSubscriptionResult]):
    user_repository: UserRepository
    plan_repository: PlanRepository
    subscription_repository: SubscriptionRepository
    order_repository: OrderRepository
    payment_repository: PaymentRepository
    payment_gateway: PaymentGateway
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: CreateSubscriptionCommand) -> CreateSubscriptionResult:
        user = await self.user_repository.get_by_id(command.user_jwt_data.id)
        if user is None:
            raise UserNotFoundError(entity_id=str(command.user_jwt_data.id))

        plan = await self.plan_repository.get_by_id(command.plan_id)
        if plan is None:
            raise PlanNotFoundError(entity_id=str(command.plan_id))

        plan.ensure_active()

        if plan.is_fixed:
            price = plan.fixed_price_for(command.currency)
            if price is None:
                raise

            if plan.limit is None:
                raise 

            limits = plan.limit

        else:
            if command.plan_draft is None:
                raise

            limits = SubscriptionLimits.create(
                duration_days=command.plan_draft.duration_days,
                trafic_bytes_limit=command.plan_draft.trafic_bytes_limit,
                max_devices=command.plan_draft.max_devices,
                features=command.plan_draft.features,
                protocols=command.plan_draft.protocols,
                strategy=command.plan_draft.strategy,
            )
            plan.validate_draft(limits)
            price = plan.calculate_price(limits)


        subscription = Subscription.create(
            user_id=command.user_jwt_data.id,
            plan_id=plan.id,
            limit=limits,
        )
        await self.subscription_repository.add(subscription)

        order = Order(
            user_id=command.user_jwt_data.id,
            subscription_id=subscription.id,
            amount=price,
            type=OrderType.NEW_SUBSCRIPTION,
            status=OrderStatus.WAITING_PAYMENT,
            subscription_limit=limits,
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
            "Subscription created",
            extra={
                "user_id": str(command.user_jwt_data.id),
                "subscription_id": str(subscription.id),
                "order_id": str(order.id),
                "payment_id": str(payment.id),
            },
        )

        return CreateSubscriptionResult(
            subscription_id=subscription.id,
            order_id=order.id,
            payment_id=payment.id,
            confirmation_url=payment.confirmation_url or "",
        )
