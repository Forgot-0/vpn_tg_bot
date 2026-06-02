from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.domain.factories.subscription_factory import SubscriptionFactory
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
    payment_gateway: PaymentGateway
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: ConfirmPaymentCommand) -> SubscriptionDTO:
        payment_intent = await self.payment_repository.get_by_external_id(command.external_payment_id)
        if payment_intent is None or payment_intent.checkout_session_id is None:
            raise

        if payment_intent.is_terminal:
            if payment_intent.status == PaymentStatus.SUCCEEDED:
                subscription = await self.subscription_repository.get_by_payment_intent(payment_intent.id)
                if subscription is None:
                    raise
                return SubscriptionDTO.from_entity(subscription)
            raise

        gateway_status = await self.payment_gateway.get_status(command.external_payment_id)

        checkout = await self.checkout_repository.get_by_id(payment_intent.checkout_session_id)
        if checkout is None:
            raise

        if checkout.server_id is None:
            raise

        server = await self.server_repository.get_by_id(checkout.server_id)
        if server is None:
            raise

        if gateway_status.status == PaymentStatus.SUCCEEDED and gateway_status.paid_at is not None:
            payment_intent.succeed(
                external_id=command.external_payment_id,
                paid_at=gateway_status.paid_at,
            )

            subscription = SubscriptionFactory.from_checkout(
                checkout=checkout,
                payment_intent=payment_intent,
            )
            # Provisioning is intentionally decoupled from payment confirmation.
            # A retryable worker should create ProvisionedAccess and then activate the subscription.
            checkout.mark_converted(payment_intent.id)

            await self.subscription_repository.add(subscription)
            await self.checkout_repository.update(checkout)

        else:
            subscription = None
            payment_intent.cancel()

        await self.payment_repository.update(payment_intent)
        await self.uow.commit()

        await self.event_bus.publish(payment_intent.pull_events())
        await self.event_bus.publish(checkout.pull_events())

        if subscription is not None:
            await self.event_bus.publish(subscription.pull_events())

        if subscription is None:
            raise

        return SubscriptionDTO.from_entity(subscription)
