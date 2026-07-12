from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.payments import ConfirmPaymentResult
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.entities.order import Order
from app.domain.entities.payment import Payment
from app.domain.entities.subscription import Subscription
from app.domain.errors import OrderNotFoundError, PaymentNotFoundError, SubscriptionNotFoundError
from app.domain.repositories.orders import OrderRepository
from app.domain.repositories.payments import PaymentRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.clock import now_utc
from app.domain.values.order import OrderType
from app.domain.values.payments import PaymentStatus
from app.domain.values.subscriptions import RenewalStrategy, SubscriptionStatus


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConfirmPaymentCommand(BaseCommand):
    external_id: str


@dataclass(frozen=True)
class ConfirmPaymentCommandHandler(BaseCommandHandler[ConfirmPaymentCommand, ConfirmPaymentResult]):
    payment_repository: PaymentRepository
    order_repository: OrderRepository
    subscription_repository: SubscriptionRepository
    payment_gateway: PaymentGateway
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: ConfirmPaymentCommand) -> ConfirmPaymentResult:
        payment = await self.payment_repository.get_by_external_id(command.external_id)
        if payment is None:
            raise PaymentNotFoundError(entity_id=command.external_id)

        if payment.is_terminal:
            logger.info(
                "Payment already processed, skipping",
                extra={"payment_id": str(payment.id), "status": payment.status.value},
            )
            return ConfirmPaymentResult(
                payment_id=payment.id,
                order_id=payment.order_id,
                status=payment.status,
            )

        status_result = await self.payment_gateway.get_status(command.external_id)

        if status_result.status == PaymentStatus.SUCCEEDED:
            return await self._apply_success(
                payment,
                external_id=status_result.external_id,
                paid_at=status_result.paid_at or now_utc(),
            )

        if status_result.status in {PaymentStatus.CANCELLED, PaymentStatus.FAILED}:
            return await self._apply_failure(payment, status=status_result.status)

        logger.info(
            "Payment not yet finalized on gateway side",
            extra={"payment_id": str(payment.id), "gateway_status": status_result.status.value},
        )
        return ConfirmPaymentResult(
            payment_id=payment.id,
            order_id=payment.order_id,
            status=status_result.status,
        )

    async def _apply_success(
        self, payment: Payment, *, external_id: str, paid_at: datetime
    ) -> ConfirmPaymentResult:
        order = await self.order_repository.get_by_id(payment.order_id)
        if order is None:
            raise OrderNotFoundError(entity_id=str(payment.order_id))

        subscription = await self.subscription_repository.get_by_id(order.subscription_id)
        if subscription is None:
            raise SubscriptionNotFoundError(entity_id=str(order.subscription_id))

        payment.succeed(external_id=external_id, paid_at=paid_at)
        order.mark_paid(paid_at=paid_at)
        self._provision_subscription(order, subscription)

        await self.payment_repository.update(payment)
        await self.order_repository.update(order)
        await self.subscription_repository.update(subscription)
        await self.uow.commit()

        await self.event_bus.publish([*payment.pull_events(), *subscription.pull_events()])

        logger.info(
            "Payment confirmed, order paid and subscription updated",
            extra={
                "payment_id": str(payment.id),
                "order_id": str(order.id),
                "subscription_id": str(subscription.id),
            },
        )

        return ConfirmPaymentResult(
            payment_id=payment.id,
            order_id=order.id,
            subscription_id=subscription.id,
            status=payment.status,
        )

    def _provision_subscription(self, order: Order, subscription: Subscription) -> None:
        if order.type == OrderType.NEW_SUBSCRIPTION:
            if subscription.status != SubscriptionStatus.ACTIVE:
                subscription.activate()
            return

        if order.type == OrderType.RENEW_SUBSCRIPTION:
            assert order.renewal_mode is not None
            strategy = RenewalStrategy(mode=order.renewal_mode)
            new_limit = order.subscription_limit or subscription.limit
            subscription.renew(strategy, new_limit)
            return

    async def _apply_failure(self, payment: Payment, *, status: PaymentStatus) -> ConfirmPaymentResult:
        order = await self.order_repository.get_by_id(payment.order_id)

        if status == PaymentStatus.CANCELLED:
            payment.cancel()
        else:
            payment.fail()
        await self.payment_repository.update(payment)

        if order is not None:
            if status == PaymentStatus.CANCELLED:
                order.mark_cancelled()
            else:
                order.mark_failed()
            await self.order_repository.update(order)

        await self.uow.commit()
        await self.event_bus.publish(payment.pull_events())

        logger.warning(
            "Payment did not succeed",
            extra={"payment_id": str(payment.id), "status": payment.status.value},
        )

        return ConfirmPaymentResult(
            payment_id=payment.id,
            order_id=payment.order_id,
            status=payment.status,
        )
