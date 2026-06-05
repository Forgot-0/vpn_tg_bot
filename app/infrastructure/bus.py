from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Type

from dishka import AsyncContainer

from app.application.event_bus import EventBus
from app.application.events.base import BaseEventHandler
from app.domain.events.base import DomainEvent




@dataclass
class EventRegisty:
    events_map: dict[Type[DomainEvent], list[Type[BaseEventHandler]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def subscribe(self, event: Type[DomainEvent], type_handlers: Iterable[Type[BaseEventHandler]]) -> None:
        self.events_map[event].extend(type_handlers)

    def get_handler_types(self, events: Iterable[DomainEvent]) -> Iterable[Type[BaseEventHandler]]:
        handler_types = []
        for event in events:
            handler_types.extend(self.events_map.get(event.__class__, []))
        return handler_types


@dataclass(eq=False)
class MediatorEventBus(EventBus):
    container: AsyncContainer

    async def publish(self, events: Iterable[DomainEvent]) -> None:
        for event in events:
            type_handlers = self.event_registy.get_handler_types([event])
            if not type_handlers:
                continue

            for type_handler in type_handlers:
                async with self.container() as requests_container:
                    handler = await requests_container.get(type_handler)
                    await handler.handle(event)
