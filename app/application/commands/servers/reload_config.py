from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.servers import BaseServerRepository
from app.domain.services.ports import BaseApiClient
from app.domain.values.users import UserRole
from app.infrastructure.api_client.router import ApiClientRouter


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReloadServerConfigCommand(BaseCommand):
    server_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class ReloadServerConfigCommandHandler(BaseCommandHandler[ReloadServerConfigCommand, None]):
    server_repository: BaseServerRepository
    api_panel: BaseApiClient
    role_access_control: RoleAccessControl

    async def handle(self, command: ReloadServerConfigCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        server = await self.server_repository.get_by_id(command.server_id)
        if server is None:
            raise

        protocol_configs = await self.api_panel.get_configs(server=server)
        server.protocol_configs.clear()
        for cnf in protocol_configs:
            server.add_protocol_config(cnf)

        logger.info(
            "Reload config server",
            extra={
                "server_id": command.server_id,
                "user_id": command.user_jwt_data.id
            }
        )