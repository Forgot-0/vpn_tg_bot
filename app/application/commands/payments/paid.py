from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.event_bus import EventBus
from app.application.interfaces.payments import PaymentGateway
from app.application.interfaces.servers import PanelClientFactory
from app.domain.factories.subscription_factory import SubscriptionFactory
from app.domain.repositories.payments import PaymentOrderRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscription_drafts import SubscriptionDraftRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.clock import now_utc
from app.domain.values.payments import PaymentStatus


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ConfirmPaymentCommand(BaseCommand):
    external_payment_id: str


@dataclass(frozen=True)
class ConfirmPaymentHandler(BaseCommandHandler[ConfirmPaymentCommand, SubscriptionDTO]):
    payment_repository: PaymentOrderRepository
    draft_repository: SubscriptionDraftRepository
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
            if payment_order.status == PaymentStatus.SUCCEEDED:
                subscription = await self.subscription_repository.get_by_payment_order(payment_order.id)
                if subscription is None:
                    raise
                return SubscriptionDTO.from_entity(subscription)
            raise

        gateway_status = await self.payment_gateway.get_status(command.external_payment_id)

        draft = await self.draft_repository.get_by_id(payment_order.draft_id)
        if draft is None:
            raise

        if draft.server_id is None:
            raise

        server = await self.server_repository.get_by_id(draft.server_id)
        if server is None:
            raise

        if gateway_status.status == PaymentStatus.SUCCEEDED and gateway_status.paid_at is not None:
            payment_order.succeed(
                external_id=command.external_payment_id,
                paid_at=gateway_status.paid_at,
            )

            panel_client = self.panel_factory.get_client(server)
            subscription = SubscriptionFactory.from_draft(
                draft=draft,
                payment_order=payment_order,
            )
            access_credentials = await panel_client.create(
                server=server,
                subscription=subscription,
            )
            subscription.activate(
                start_date=now_utc().date(),
                purchased_price=payment_order.amount,
                access_credentials=access_credentials,
            )
            server.increment_clients()
            draft.mark_converted(payment_order.id)

            await self.subscription_repository.add(subscription)
            await self.server_repository.update(server)
            await self.draft_repository.update(draft)

        else:
            subscription = None
            payment_order.cancel()

        await self.payment_repository.update(payment_order)
        await self.uow.commit()

        await self.event_bus.publish(payment_order.pull_events())
        await self.event_bus.publish(draft.pull_events())

        if subscription is not None:
            await self.event_bus.publish(subscription.pull_events())

        if subscription is None:
            raise

        return SubscriptionDTO.from_entity(subscription)
