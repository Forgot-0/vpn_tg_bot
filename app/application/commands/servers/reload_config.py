from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.users import UserRole
from app.infrastructure.api_client.factory import ApiClientFactory


@dataclass(frozen=True)
class ReloadServerConfigCommand(BaseCommand):
    server_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class ReloadServerConfigCommandHandler(BaseCommandHandler[ReloadServerConfigCommand, None]):
    server_repository: BaseServerRepository
    api_panel_factory: ApiClientFactory
    role_access_control: RoleAccessControl

    async def handle(self, command: ReloadServerConfigCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        server = await self.server_repository.get_by_id(command.server_id)
        if server is None:
            raise

        api_panel = self.api_panel_factory.get(server.api_type)

        protocol_configs = await api_panel.get_configs(server=server)
        server.protocol_configs.clear()
        for cnf in protocol_configs:
            server.add_protocol_config(cnf)