from dataclasses import dataclass
from json import loads

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.server import Country, Server
from domain.repositories.servers import BaseServerRepository



@dataclass(frozen=True)
class CreateServerCommand(BaseCommand):
    text: str


@dataclass(frozen=True)
class CreateServerCommandHandler(BaseCommandHandler[CreateServerCommand, None]):
    server_repository: BaseServerRepository

    async def handle(self, command: CreateServerCommand) -> None:
        document = loads(command.text)

        server = Server(
            ip=document['ip'],
            port=document['port'],
            domain=document['domain'],
            limit=document['limit'],
            pbk=document['pbk'],
            country=Country(document['country']),
            free=document['free'],

            name=document['name'],
            panel_port=document['panel_port'],
            panel_path=document['panel_path']
        )

        await self.server_repository.create(server=server)