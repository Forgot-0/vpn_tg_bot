from dataclasses import dataclass
from typing import Any

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.server import Server
from domain.repositories.servers import BaseServerRepository
from domain.values.servers import ApiType, Region
from infrastructure.api_client.factory import ApiClientFactory


@dataclass(frozen=True)
class CreateServerCommand(BaseCommand):
    limin: int
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

    async def handle(self, command: CreateServerCommand) -> None:
        api_type = ApiType(command.api_type)
        api_panel = self.api_panel_factory.get(api_type)

        server = Server.create(
            limit=command.limin,
            region=Region(
                flag=command.flag,
                name=command.name,
                code=command.code,
            ),
            api_type=api_type,
            auth_credits=command.auth_credits,
            api_config=command.api_config
        )

        protocol_configs = await api_panel.get_configs(server=server)
        for cnf in protocol_configs:
            server.add_protocol_config(cnf)

        await self.server_repository.create(server=server)