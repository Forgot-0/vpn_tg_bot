from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from domain.events.base import BaseEvent
from application.commands.base import CR, CT, BaseCommand, BaseCommandHandler
from application.events.base import ER, ET, BaseEventHandler
from application.exception import HandlersNotRegisteredExeption
from application.queries.base import QR, QT, BaseQuery, BaseQueryHandler
from infrastructure.mediator.event_mediator import EventMediator




@dataclass(eq=False)
class Mediator(EventMediator):
    events_map: dict[ET, list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    commands_map: dict[CT, list[BaseCommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[BaseEventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)        

    def register_command(self, command: CT, command_handlers: Iterable[BaseCommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]):
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers = self.events_map.get(event.__class__)
            if not handlers:
                raise HandlersNotRegisteredExeption(event.__class__)
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        handlers = self.commands_map.get(command.__class__)
        if not handlers:
            raise HandlersNotRegisteredExeption(command.__class__)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query=query)