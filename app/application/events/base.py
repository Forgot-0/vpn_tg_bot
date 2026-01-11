from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from app.domain.events.base import BaseEvent


@dataclass(frozen=True)
class IntegrationEvent(BaseEvent, ABC):
    ...


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class BaseEventHandler(ABC, Generic[ET, ER]):

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...

