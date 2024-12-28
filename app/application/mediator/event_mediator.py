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
from typing import TYPE_CHECKING, Generic

from domain.events.base import BaseEvent

if TYPE_CHECKING:
    from application.events.base import (
        ER,
        ET,
        BaseEventHandler,
    )



@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict['ET', 'BaseEventHandler'] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(self, event: 'ET', event_handlers: Iterable['BaseEventHandler']):
        ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable['ER']:
        ...