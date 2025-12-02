from dataclasses import dataclass, field
from typing import Any

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.server import Server
from domain.repositories.servers import BaseServerRepository
from domain.services.servers import SecureService
from domain.values.servers import APIConfig, APICredits, ApiType, Region
from infrastructure.api_client.factory import ApiClientFactory


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


@dataclass(frozen=True)
class CreateServerCommandHandler(BaseCommandHandler[CreateServerCommand, None]):
    server_repository: BaseServerRepository
    api_panel_factory: ApiClientFactory
    secure_service: SecureService

    async def handle(self, command: CreateServerCommand) -> None:
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