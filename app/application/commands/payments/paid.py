from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.commands.subscriptions.renew import (
    RenewSubscriptionCommand,
    RenewSubscriptionHandler,
)
from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.errors import (
    CheckoutNotFoundError,
    PaymentAlreadyTerminalError,
    PaymentNotFoundError,
    ServerNotFoundError,
    SubscriptionNotFoundError,
)
from app.domain.entities.subscription import Subscription
from app.domain.factories.subscription_factory import SubscriptionFactory
from app.domain.values.checkouts import CheckoutIntent
from app.domain.repositories.payments import PaymentIntentRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.checkouts import CheckoutSessionRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.values.payments import PaymentStatus


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConfirmPaymentCommand(BaseCommand):
    external_payment_id: str


@dataclass(frozen=True)
class ConfirmPaymentHandler(BaseCommandHandler[ConfirmPaymentCommand, SubscriptionDTO]):
    payment_repository: PaymentIntentRepository
    checkout_repository: CheckoutSessionRepository
    subscription_repository: SubscriptionRepository
    server_repository: VPNServerRepository
    renew_handler: RenewSubscriptionHandler
    payment_gateway: PaymentGateway
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: ConfirmPaymentCommand) -> SubscriptionDTO:
        payment_intent = await self.payment_repository.get_by_external_id(command.external_payment_id)

        if payment_intent is None or payment_intent.checkout_session_id is None:
            raise PaymentNotFoundError(entity_id=command.external_payment_id)

        checkout = await self.checkout_repository.get_by_id(payment_intent.checkout_session_id)
        if checkout is None:
            raise CheckoutNotFoundError(entity_id=str(payment_intent.checkout_session_id))

        is_renewal = checkout.metadata.get("intent") == CheckoutIntent.RENEWAL.value

        if payment_intent.is_terminal:
            if payment_intent.status == PaymentStatus.SUCCEEDED:
                if is_renewal:
                    subscription = await self._get_renewal_subscription(checkout)
                else:
                    subscription = await self.subscription_repository.get_by_payment_intent(
                        payment_intent.id,
                    )
                if subscription is None:
                    raise SubscriptionNotFoundError(entity_id=str(payment_intent.id))
                return SubscriptionDTO.from_entity(subscription)
            raise PaymentAlreadyTerminalError

        gateway_status = await self.payment_gateway.get_status(command.external_payment_id)

        if checkout.server_id is None:
            raise ServerNotFoundError(entity_id=str(checkout.server_id))

        server = await self.server_repository.get_by_id(checkout.server_id)
        if server is None:
            raise ServerNotFoundError(entity_id=str(checkout.server_id))

        if gateway_status.status == PaymentStatus.SUCCEEDED and gateway_status.paid_at is not None:
            if is_renewal:
                result = await self.renew_handler.handle(
                    RenewSubscriptionCommand(
                        subscription_id=UUID(str(checkout.metadata["subscription_id"])),
                        payment_intent_id=payment_intent.id,
                        renewed_at=gateway_status.paid_at,
                        external_payment_id=command.external_payment_id,
                    )
                )
                return result.subscription

            payment_intent.succeed(
                external_id=command.external_payment_id,
                paid_at=gateway_status.paid_at,
            )

            subscription = SubscriptionFactory.from_checkout(
                checkout=checkout,
                payment_intent=payment_intent,
            )
            checkout.mark_converted(payment_intent.id)

            await self.payment_repository.update(payment_intent)
            await self.subscription_repository.add(subscription)
            await self.checkout_repository.update(checkout)
            await self.uow.commit()

            await self.event_bus.publish(payment_intent.pull_events())
            await self.event_bus.publish(checkout.pull_events())
            await self.event_bus.publish(subscription.pull_events())
            return SubscriptionDTO.from_entity(subscription)

        payment_intent.cancel()
        await self.payment_repository.update(payment_intent)
        await self.uow.commit()
        await self.event_bus.publish(payment_intent.pull_events())
        raise PaymentNotFoundError(entity_id=command.external_payment_id)

    async def _get_renewal_subscription(self, checkout) -> Subscription | None:
        subscription_id = checkout.metadata.get("subscription_id")
        if subscription_id is None:
            return None
        return await self.subscription_repository.get_by_id(UUID(str(subscription_id)))
