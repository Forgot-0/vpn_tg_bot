
from collections.abc import Iterable
from dataclasses import dataclass

from dishka import AsyncContainer

from app.application.commands.base import CR, BaseCommand
from app.application.queries.base import QR, BaseQuery
from app.infrastructure.mediator.base import BaseMediator




@dataclass(eq=False)
class DishkaMediator(BaseMediator):
    container: AsyncContainer

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        result = []

        handler_registy = self.command_registy.get_handler_types(command)
        if not handler_registy:
            raise 

        for handler_type in handler_registy:
            async with self.container() as requests_container:
                handler = await requests_container.get(handler_type)
                result.append(await handler.handle(command))

        return result

    async def handle_query(self, query: BaseQuery) -> QR:
        handler_registy = self.query_registy.get_handler_types(query)

        async with self.container() as requests_container:
            handler = await requests_container.get(handler_registy)
            return await handler.handle(query)
