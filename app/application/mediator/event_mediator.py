from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from domain.events.base import BaseEvent

from application.events.base import (
    ER,
    ET,
    BaseEventHandler,
)



@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[ET, list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(self, event: 'ET', event_handlers: Iterable[BaseEventHandler[ET, ER]]):
        ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable['ER']:
        ...