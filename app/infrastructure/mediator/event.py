from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Type

from dishka import AsyncContainer

from app.application.events.base import BaseEventHandler
from app.domain.events.base import BaseEvent




@dataclass
class EventRegisty:
    events_map: dict[Type[BaseEvent], list[Type[BaseEventHandler]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def subscribe(self, event: Type[BaseEvent], type_handlers: Iterable[Type[BaseEventHandler]]) -> None:
        self.events_map[event].extend(type_handlers)

    def get_handler_types(self, events: Iterable[BaseEvent]) -> Iterable[Type[BaseEventHandler]]:
        handler_types = []
        for event in events:
            handler_types.extend(self.events_map.get(event.__class__, []))
        return handler_types


@dataclass(eq=False)
class BaseEventBus(ABC):
    event_registy: EventRegisty

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> None:
        ...


@dataclass(eq=False)
class MediatorEventBus(BaseEventBus):
    container: AsyncContainer

    async def publish(self, events: Iterable[BaseEvent]) -> None:
        for event in events:
            type_handlers = self.event_registy.get_handler_types([event])
            if not type_handlers:
                continue

            for type_handler in type_handlers:
                async with self.container() as requests_container:
                    handler = await requests_container.get(type_handler)
                    await handler.handle(event)
