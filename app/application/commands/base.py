from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from application.mediator.event_mediator import EventMediator


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...


CT = TypeVar('CT', bound=BaseCommand)
CR = TypeVar('CR', bound=Any)


@dataclass(frozen=True)
class BaseCommandHandler(ABC, Generic[CT, CR]):
    mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...
