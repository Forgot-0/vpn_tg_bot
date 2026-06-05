from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.servers import AddServerResultDTO
from app.application.event_bus import EventBus
from app.application.interfaces.servers import PanelClientFactory
from app.domain.entities.server import CapacityPolicy, VPNServer
from app.domain.errors import (
    PanelConnectionInactiveError,
    PanelConnectionNotFoundError,
)
from app.domain.repositories.panel_connections import PanelConnectionRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.values.servers import FeatureCode, ProtocolCode


@dataclass(frozen=True)
class AddNewServerCommand(BaseCommand):
    name: str
    region_code: str
    panel_connection_id: UUID

    location_id: UUID | None = None
    server_group_id: UUID | None = None
    max_clients: int | None = None
    weight: int = 100

    protocol_codes: frozenset[str] = frozenset()
    feature_codes: frozenset[str] = frozenset()
    tags: frozenset[str] = frozenset()
    panel_config: dict[str, Any] = field(default_factory=dict)

    is_active: bool = True
    sync_from_panel: bool = True


@dataclass(frozen=True)
class AddNewServerCommandHandler(
    BaseCommandHandler[AddNewServerCommand, AddServerResultDTO]
):
    server_repository: VPNServerRepository
    connection_repository: PanelConnectionRepository
    panel_factory: PanelClientFactory
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: AddNewServerCommand) -> AddServerResultDTO:
        connection = await self.connection_repository.get_by_id(command.panel_connection_id)
        if connection is None:
            raise PanelConnectionNotFoundError(entity_id=str(command.panel_connection_id))

        if not connection.is_active:
            raise PanelConnectionInactiveError

        supported_protocols = frozenset(
            ProtocolCode(code) for code in command.protocol_codes
        )
        supported_features = frozenset(
            FeatureCode(code) for code in command.feature_codes
        )
        current_clients = 0
        panel_config = dict(command.panel_config)

        if command.sync_from_panel:
            draft = VPNServer(
                id=uuid4(),
                name=command.name,
                region_code=command.region_code,
                panel_connection_id=command.panel_connection_id,
                panel_config=panel_config,
            )
            panel_client = self.panel_factory.get_client(connection)
            panel_info = await panel_client.get_info(server=draft, connection=connection)

            if panel_info.supported_protocols:
                supported_protocols = panel_info.supported_protocols
            if panel_info.supported_features:
                supported_features = panel_info.supported_features
            if panel_info.panel_config:
                panel_config = {**panel_config, **panel_info.panel_config}
            current_clients = panel_info.current_clients

        server = VPNServer.create(
            name=command.name,
            region_code=command.region_code,
            panel_connection_id=command.panel_connection_id,
            location_id=command.location_id,
            server_group_id=command.server_group_id,
            capacity_policy=CapacityPolicy(
                max_clients=command.max_clients,
                weight=command.weight,
            ),
            supported_protocols=supported_protocols,
            supported_features=supported_features,
            is_active=command.is_active,
            max_clients=command.max_clients,
            current_clients=current_clients,
            tags=command.tags,
            panel_config=panel_config,
        )

        await self.server_repository.add(server)
        await self.uow.commit()
        await self.event_bus.publish(server.pull_events())

        return AddServerResultDTO.from_entity(server)
