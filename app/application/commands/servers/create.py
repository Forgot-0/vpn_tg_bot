from dataclasses import dataclass
from typing import Any

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.server import Server
from domain.repositories.servers import BaseServerRepository
from domain.services.servers import SecureService
from domain.values.servers import ApiType, Region
from infrastructure.api_client.factory import ApiClientFactory


@dataclass(frozen=True)
class CreateServerCommand(BaseCommand):
    limit: int
    flag: str
    name: str
    code: str
    api_type: str
    api_config: dict[str, Any]
    auth_credits: dict[str, str]


@dataclass(frozen=True)
class CreateServerCommandHandler(BaseCommandHandler[CreateServerCommand, None]):
    server_repository: BaseServerRepository
    api_panel_factory: ApiClientFactory
    secure_service: SecureService

    async def handle(self, command: CreateServerCommand) -> None:
        api_type = ApiType(command.api_type)
        api_panel = self.api_panel_factory.get(api_type)

        encrypt_creadits = {}
        for key, val in command.auth_credits.items():
            encrypt_creadits[key] = self.secure_service.encrypt(val)

        server = Server.create(
            limit=command.limit,
            region=Region(
                flag=command.flag,
                name=command.name,
                code=command.code,
            ),
            api_type=api_type,
            auth_credits=encrypt_creadits,
            api_config=command.api_config
        )

        protocol_configs = await api_panel.get_configs(server=server)
        for cnf in protocol_configs:
            server.add_protocol_config(cnf)

        await self.server_repository.create(server=server)