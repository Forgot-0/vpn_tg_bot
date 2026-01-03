from dataclasses import dataclass, field
import logging
from typing import Any

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.entities.server import Server
from app.domain.repositories.servers import BaseServerRepository
from app.domain.services.servers import SecureService
from app.domain.values.servers import APIConfig, APICredits, ApiType, Region
from app.domain.values.users import UserRole
from app.infrastructure.api_client.factory import ApiClientFactory
from app.application.exception import ForbiddenException


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateServerCommand(BaseCommand):
    limit: int
    code: str
    api_type: str

    ip: str
    panel_port: int
    panel_path: str
    domain: str | None = field(default=None, kw_only=True)

    username: str
    password: str
    twoFactorCode: str | None = field(default=None, kw_only=True)

    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class CreateServerCommandHandler(BaseCommandHandler[CreateServerCommand, None]):
    server_repository: BaseServerRepository
    api_panel_factory: ApiClientFactory
    secure_service: SecureService
    role_access_control: RoleAccessControl

    async def handle(self, command: CreateServerCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        api_type = ApiType(command.api_type)
        api_panel = self.api_panel_factory.get(api_type)

        encrypt_creadits = APICredits(
            username=self.secure_service.encrypt(command.username),
            password=self.secure_service.encrypt(command.password),
            twoFactorCode=self.secure_service.encrypt(command.twoFactorCode) if command.twoFactorCode else None
        )

        server = Server.create(
            limit=command.limit,
            region=Region.region_by_code(command.code),
            api_type=api_type,
            auth_credits=encrypt_creadits,
            api_config=APIConfig(
                ip=command.ip,
                panel_port=command.panel_port,
                panel_path=command.panel_path,
                domain=command.domain
            )
        )

        protocol_configs = await api_panel.get_configs(server=server)
        for cnf in protocol_configs:
            server.add_protocol_config(cnf)

        await self.server_repository.create(server=server)
        logger.info(
            "Create Server", extra={
                "server_id": server.id,
                "region_code": server.region.code,
                "protocols": [protocol.value for  protocol in server.protocol_configs.keys()],
                "user_id": command.user_jwt_data.id
                }
        )