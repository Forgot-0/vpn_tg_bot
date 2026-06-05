from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from app.domain.events.base import DomainEvent



ET = TypeVar('ET', bound=DomainEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class BaseEventHandler(ABC, Generic[ET, ER]):

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...

