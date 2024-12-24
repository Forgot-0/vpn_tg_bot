from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.events.base import BaseEvent




@dataclass(kw_only=True)
class AggregateRoot(ABC):
    _events: list[BaseEvent] = field(
        default_factory=list,
        init=False, repr=False, hash=False, compare=False,
    )

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events