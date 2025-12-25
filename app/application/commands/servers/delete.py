
from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class DeleteServerCommand(BaseCommand):
    server_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class DeleteServerCommandHandler(BaseCommandHandler[DeleteServerCommand, None]):
    server_repository: BaseServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, command: DeleteServerCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        await self.server_repository.delete_by_id(command.server_id)
