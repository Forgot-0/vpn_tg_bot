from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.application.interfaces.servers import PanelClientFactory
from app.domain.repositories.payments import PaymentOrderRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.clock import now_utc


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ConfirmPaymentCommand(BaseCommand):
    external_payment_id: str


@dataclass(frozen=True)
class ConfirmPaymentHandler(BaseCommandHandler[ConfirmPaymentCommand, SubscriptionDTO]):
    payment_repository: PaymentOrderRepository
    subscription_repository: SubscriptionRepository
    server_repository: VPNServerRepository
    payment_gateway: PaymentGateway
    panel_factory: PanelClientFactory
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: ConfirmPaymentCommand) -> SubscriptionDTO:
        payment_order = await self.payment_repository.get_by_external_id(command.external_payment_id)
        if payment_order is None:
            raise 

        if payment_order.is_terminal:
            sub = await self.subscription_repository.get_by_id(payment_order.subscription_id)
            if sub is None:
                raise 
            return SubscriptionDTO.from_entity(sub)
 
        gateway_status = await self.payment_gateway.get_status(command.external_payment_id)

        subscription = await self.subscription_repository.get_by_id(payment_order.subscription_id)
        if subscription is None:
            raise 

        server = await self.server_repository.get_by_id(subscription.server_id)
        if server is None:
            raise 

        from app.domain.values.payments import PaymentStatus
        if gateway_status.status == PaymentStatus.SUCCEEDED and gateway_status.paid_at is not None:
            payment_order.succeed(
                external_id=command.external_payment_id,
                paid_at=gateway_status.paid_at,
            )

            panel_client = self.panel_factory.get_client(server)
            access_credentials = await panel_client.create(server, subscription)

            subscription.activate(
                start_date=now_utc().today(),
                purchased_price=payment_order.amount,
                access_credentials=access_credentials,
            )
            server.increment_clients()

        elif gateway_status.status in {PaymentStatus.CANCELLED, PaymentStatus.FAILED}:
            payment_order.cancel()
            subscription.cancel()

        await self.payment_repository.update(payment_order)
        await self.subscription_repository.update(subscription)
        await self.server_repository.update(server)
        await self.uow.commit()

        await self.event_bus.publish(payment_order.pull_events())
        await self.event_bus.publish(subscription.pull_events())

        return SubscriptionDTO.from_entity(subscription)
