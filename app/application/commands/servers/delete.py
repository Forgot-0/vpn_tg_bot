from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users import UserJWTData
from app.domain.errors import ServerNotFoundError
from app.domain.repositories.servers import ServerRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeleteServerCommand(BaseCommand):
    user_jwt_data: UserJWTData
    server_id: UUID


@dataclass(frozen=True)
class DeleteServerCommandHandler(BaseCommandHandler[DeleteServerCommand, None]):
    server_repository: ServerRepository
    access_service: RoleAccessControl
    uow: UnitOfWork

    async def handle(self, command: DeleteServerCommand) -> None:
        if not self.access_service.can_action(command.user_jwt_data.role, UserRole.ADMIN):
            raise 

        server = await self.server_repository.get_by_id(command.server_id)
        if server is None:
            raise ServerNotFoundError(entity_id=str(command.server_id))

        await self.server_repository.delete(command.server_id)
        await self.uow.commit()

        logger.info(
            "Deleted server",
            extra={
                "deleted_by": str(command.user_jwt_data.id),
                "server_id": str(command.server_id),
            },
        )
