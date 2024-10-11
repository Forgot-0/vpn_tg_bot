from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.subscription import Subscription


@dataclass
class BaseSubscriptionRepository(ABC):

    @abstractmethod
    async def create(self, subscription: Subscription) -> None:
        ...

    @abstractmethod
    async def pay(self, id: UUID) -> None:
        ...

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> Subscription | None:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Subscription | None:
        ...
