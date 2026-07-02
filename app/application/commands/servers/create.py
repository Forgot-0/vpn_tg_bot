from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users import UserJWTData
from app.domain.entities.server import VPNServer
from app.domain.repositories.servers import ServerRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.servers import (
    Capacity,
    FeatureCode,
    Location,
    PanelCredentials,
    PanelEndpoint,
    PanelType,
    ProtocolCode,
)
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateServerCommand(BaseCommand):
    user_jwt_data: UserJWTData

    name: str
    region_code: str
    panel_type: PanelType
    panel_host: str
    panel_port: int
    panel_path: str = "/"
    panel_use_ssl: bool = True
    panel_username: str | None = None
    panel_password: str | None = None

    max_clients: int = 0
    supported_protocols: set[ProtocolCode] = field(default_factory=set)
    supported_features: set[FeatureCode] = field(default_factory=set)
    tags: list[str] = field(default_factory=list)
    is_active: bool = True


@dataclass(frozen=True)
class CreateServerCommandHandler(BaseCommandHandler[CreateServerCommand, VPNServer]):
    server_repository: ServerRepository
    access_service: RoleAccessControl
    uow: UnitOfWork

    async def handle(self, command: CreateServerCommand) -> VPNServer:
        if not self.access_service.can_action(command.user_jwt_data.role, UserRole.ADMIN):
            raise 

        server = VPNServer(
            name=command.name,
            capacity=Capacity(max_client=command.max_clients, free=0),
            panel_type=command.panel_type,
            panel_endpoint=PanelEndpoint(
                host=command.panel_host,
                port=command.panel_port,
                path=command.panel_path,
                use_ssl=command.panel_use_ssl,
            ),
            panel_credentials=PanelCredentials(
                username=command.panel_username,
                password=command.panel_password,
            ),
            locations={Location(code=command.region_code, name=command.region_code)},
            support_protocols=command.supported_protocols,
            support_features=command.supported_features,
            is_active=command.is_active,
            tags=command.tags,
        )

        await self.server_repository.add(server, region_code=command.region_code)
        await self.uow.commit()

        logger.info(
            "Created server",
            extra={
                "created_by": str(command.user_jwt_data.id),
                "server_id": str(server.id),
                "region_code": command.region_code,
            },
        )
        return server
