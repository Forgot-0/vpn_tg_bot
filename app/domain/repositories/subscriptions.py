from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.subscription import Subscription


@dataclass
class BaseSubscriptionRepository(ABC):

    @abstractmethod
    async def create(self, subscription: Subscription) -> None: ...

    @abstractmethod
    async def deactivate(self, id: UUID) -> None: ...

    @abstractmethod
    async def activate(self, id: UUID) -> None: ...

    @abstractmethod
    async def get(self) -> list[Subscription]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Subscription | None: ...