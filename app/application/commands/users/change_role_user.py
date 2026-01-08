from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException, NotFoundException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId, UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ChangeRoleUserCommand(BaseCommand):
    user_jwt_data: UserJWTData
    user_to: UUID
    role: str


@dataclass(frozen=True)
class ChangeRoleUserCommandHandler(BaseCommandHandler[ChangeRoleUserCommand, None]):
    user_repository: BaseUserRepository
    role_access_control: RoleAccessControl

    async def handle(self, command: ChangeRoleUserCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        user = await self.user_repository.get_by_id(UserId(command.user_to))
        if user is None:
            raise NotFoundException()

        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=user.role
        ): raise ForbiddenException()

        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole(command.role)
        ): raise ForbiddenException()

        user.change_role(role=UserRole(command.role))

        await self.user_repository.update(user)

        logger.info(
            "Change role user",
            extra={
                "user_by": command.user_jwt_data.id,
                "user_to": command.user_to,
                "role": command.role
            }
        )
