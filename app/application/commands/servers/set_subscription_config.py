from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.servers import SubscriptionConfig
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetSubscriptionConfigServerCommand(BaseCommand):
    server_id: UUID
    url: str
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class SetSubscriptionConfigServerCommandHandler(BaseCommandHandler[SetSubscriptionConfigServerCommand, None]):
    server_repository: BaseServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, command: SetSubscriptionConfigServerCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        server = await self.server_repository.get_by_id(command.server_id)
        if server is None:
            raise

        server.set_new_subscription_config(
            SubscriptionConfig.from_url(command.url)
        )
        await self.server_repository.update(server)

        logger.info(
            "Set subscription config server",
            extra={
                "server_id": command.server_id,
                "url": command.url,
                "user_by": command.user_jwt_data.id
            }
        )
