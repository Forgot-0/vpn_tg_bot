from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar



@dataclass(frozen=True)
class BaseCommand(ABC):
    ...


CT = TypeVar('CT', bound=BaseCommand)
CR = TypeVar('CR', bound=Any)


@dataclass(frozen=True)
class BaseCommandHandler(ABC, Generic[CT, CR]):

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...