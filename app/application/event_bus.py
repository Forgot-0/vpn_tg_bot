from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass

from app.domain.events.base import DomainEvent
from app.infrastructure.bus import EventRegisty


@dataclass(eq=False)
class EventBus(ABC):
    event_registy: EventRegisty

    @abstractmethod
    async def publish(self, events: Iterable[DomainEvent]) -> None:
        ...
