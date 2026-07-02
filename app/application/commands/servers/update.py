from __future__ import annotations

import logging
from dataclasses import dataclass, field
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users import UserJWTData
from app.domain.errors import ServerNotFoundError
from app.domain.repositories.servers import ServerRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.servers import Capacity, FeatureCode, PanelType, ProtocolCode
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UpdateServerCommand(BaseCommand):
    user_jwt_data: UserJWTData
    server_id: UUID

    name: str | None = None
    region_code: str | None = None
    panel_type: PanelType | None = None
    panel_host: str | None = None
    panel_port: int | None = None
    panel_path: str | None = None
    panel_use_ssl: bool | None = None
    panel_username: str | None = None
    panel_password: str | None = None
    max_clients: int | None = None
    supported_protocols: set[ProtocolCode] | None = None
    supported_features: set[FeatureCode] | None = None
    tags: list[str] | None = None
    is_active: bool | None = None


@dataclass(frozen=True)
class UpdateServerCommandHandler(BaseCommandHandler[UpdateServerCommand, None]):
    server_repository: ServerRepository
    access_service: RoleAccessControl
    uow: UnitOfWork

    async def handle(self, command: UpdateServerCommand) -> None:
        if not self.access_service.can_action(command.user_jwt_data.role, UserRole.ADMIN):
            raise 

        server = await self.server_repository.get_by_id(command.server_id)
        if server is None:
            raise ServerNotFoundError(entity_id=str(command.server_id))

        if command.name is not None:
            server.name = command.name

        if command.panel_type is not None:
            server.panel_type = command.panel_type

        if any(v is not None for v in (command.panel_host, command.panel_port, command.panel_path, command.panel_use_ssl)):
            server.panel_endpoint = type(server.panel_endpoint)(
                host=command.panel_host or server.panel_endpoint.host,
                port=command.panel_port or server.panel_endpoint.port,
                path=command.panel_path or server.panel_endpoint.path,
                use_ssl=command.panel_use_ssl if command.panel_use_ssl is not None else server.panel_endpoint.use_ssl,
            )

        if command.panel_username is not None or command.panel_password is not None:
            server.panel_credentials = type(server.panel_credentials)(
                username=command.panel_username or server.panel_credentials.username,
                password=command.panel_password or server.panel_credentials.password,
            )

        if command.max_clients is not None:
            server.capacity = Capacity(max_client=command.max_clients, free=server.capacity.free)

        if command.supported_protocols is not None:
            server.support_protocols = command.supported_protocols

        if command.supported_features is not None:
            server.support_features = command.supported_features

        if command.tags is not None:
            server.tags = command.tags

        if command.is_active is not None:
            server.is_active = command.is_active

        await self.server_repository.update(server, region_code=command.region_code)
        await self.uow.commit()

        logger.info(
            "Updated server",
            extra={
                "updated_by": str(command.user_jwt_data.id),
                "server_id": str(command.server_id),
            },
        )
