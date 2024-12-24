from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.server import Server
from domain.repositories.servers import BaseServerRepository
from infrastructure.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class DeletNotActiveUserCommand(BaseCommand):
    ...


@dataclass(frozen=True)
class DeletNotActiveUserCommandHandler(BaseCommandHandler[DeletNotActiveUserCommand, None]):
    server_repository: BaseServerRepository
    vpn_service: BaseVpnService

    async def handle(self, command: DeletNotActiveUserCommand) -> None:
        servers: list[Server] = await self.server_repository.get_all()
        for server in servers:
            await self.vpn_service.delete_not_active(server=server)
            count = len((await self.vpn_service.get_list(server=server))['obj'][0]['clientStats'])
            await self.server_repository.set_free(server_id=server.id, new_free=server.limit-count)