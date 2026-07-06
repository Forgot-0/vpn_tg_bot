from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Type

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
class EventBus(ABC):
    event_registy: EventRegisty

    @abstractmethod
    async def publish(self, events: Iterable[DomainEvent]) -> None:
        ...
