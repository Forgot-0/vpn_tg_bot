from dataclasses import dataclass
from json import loads

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.server import Country, Server
from infra.repositories.servers.base import BaseServerRepository


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

            uri_login=document['uri_login'],
            uri_create=document['uri_create'],
            uri_delete=document['uri_delete'],
            uri_update=document['uri_update'],
            uri_get=document['uri_get'],
        )
        await self.server_repository.create(server=server)