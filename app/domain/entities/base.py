from __future__ import annotations

from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field

from app.domain.events.base import DomainEvent


@dataclass(kw_only=True)
class AggregateRoot(ABC):
    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        ...

    def register_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events = copy(self._events)
        self._events.clear()
        return events