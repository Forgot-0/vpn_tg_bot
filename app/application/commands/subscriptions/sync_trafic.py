from dataclasses import dataclass
from decimal import Decimal
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.event_bus import EventBus
from app.application.interfaces.servers import PanelClientFactory
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork



logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SyncSubscriptionTrafficCommand(BaseCommand):
    subscription_id: UUID

@dataclass(frozen=True)
class SyncSubscriptionTrafficHandler(BaseCommandHandler[SyncSubscriptionTrafficCommand, Decimal]):
    subscription_repository: SubscriptionRepository
    server_repository: VPNServerRepository
    panel_factory: PanelClientFactory
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: SyncSubscriptionTrafficCommand) -> Decimal:
        subscription = await self.subscription_repository.get_by_id(command.subscription_id)
        if subscription is None:
            raise 

        server = await self.server_repository.get_by_id(subscription.server_id)
        if server is None:
            raise 

        panel_client = self.panel_factory.get_client(server)
        used_gb = await panel_client.sync_traffic(server, subscription)

        delta = used_gb - subscription.used_traffic_gb
        if delta > Decimal("0"):
            subscription.consume_traffic(delta)
            await self.subscription_repository.update(subscription)
            await self.uow.commit()
            await self.event_bus.publish(subscription.pull_events())

        return subscription.used_traffic_gb
