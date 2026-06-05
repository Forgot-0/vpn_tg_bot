from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.access import ProvisionSubscriptionResultDTO
from app.application.event_bus import EventBus
from app.application.interfaces.servers import PanelClientFactory
from app.domain.errors import (
    NoAvailableServerError,
    PanelConnectionInactiveError,
    PanelConnectionNotFoundError,
    ProvisioningFailedError,
    ServerNotFoundError,
    SubscriptionMissingServerError,
    SubscriptionNotFoundError,
    SubscriptionNotReadyForProvisioningError,
)
from app.domain.repositories.access import ProvisionedAccessRepository
from app.domain.repositories.panel_connections import PanelConnectionRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.clock import now_utc
from app.domain.values.subscriptions import SubscriptionStatus


@dataclass(frozen=True)
class ProvisionSubscriptionAccessCommand(BaseCommand):
    subscription_id: UUID


@dataclass(frozen=True)
class ProvisionSubscriptionAccessHandler(
    BaseCommandHandler[ProvisionSubscriptionAccessCommand, ProvisionSubscriptionResultDTO]
):
    subscription_repository: SubscriptionRepository
    server_repository: VPNServerRepository
    connection_repository: PanelConnectionRepository
    access_repository: ProvisionedAccessRepository
    panel_factory: PanelClientFactory
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(
        self, command: ProvisionSubscriptionAccessCommand,
    ) -> ProvisionSubscriptionResultDTO:
        subscription = await self.subscription_repository.get_by_id(command.subscription_id)
        if subscription is None:
            raise SubscriptionNotFoundError(entity_id=str(command.subscription_id))


        if subscription.status not in {
            SubscriptionStatus.PENDING_PROVISIONING,
            SubscriptionStatus.PROVISIONING_FAILED
        }:
            raise SubscriptionNotReadyForProvisioningError(
                status_value=subscription.status.value,
            )

        if subscription.server_id is None:
            raise SubscriptionMissingServerError


        if subscription.status == SubscriptionStatus.PROVISIONING_FAILED:
            subscription.retry_provisioning()

        subscription.begin_provisioning()

        server = await self.server_repository.get_by_id(subscription.server_id)
        if server is None or server.is_active is False:
            raise ServerNotFoundError(entity_id=str(subscription.server_id))

        if not server.can_accommodate(subscription.spec):
            raise NoAvailableServerError

        connection = await self.connection_repository.get_by_id(server.panel_connection_id)
        if connection is None:
            raise PanelConnectionNotFoundError(entity_id=str(server.panel_connection_id))

        if not connection.is_active:
            raise PanelConnectionInactiveError

        panel_client = self.panel_factory.get_client(connection)

        try:
            access = await panel_client.create(
                server=server,
                connection=connection,
                subscription=subscription,
            )
        except Exception as exc:
            reason = str(exc)
            subscription.mark_provisioning_failed(reason=reason)
            await self.subscription_repository.update(subscription)
            await self.uow.commit()
            await self.event_bus.publish(subscription.pull_events())
            raise ProvisioningFailedError(reason=reason) from exc

        await self.access_repository.add(access)

        subscription.complete_provisioning(
            provisioned_access_id=access.id,
            credentials=access.credentials,
            start_date=now_utc().date(),
        )
        server.increment_clients()

        await self.subscription_repository.update(subscription)
        await self.server_repository.update(server)
        await self.uow.commit()

        await self.event_bus.publish(access.pull_events())
        await self.event_bus.publish(subscription.pull_events())

        return ProvisionSubscriptionResultDTO.create(
            subscription_id=subscription.id,
            subscription_status=subscription.status.value,
            access=access,
        )
