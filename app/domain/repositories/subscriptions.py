from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.subscription import Subscription
from domain.values.subscriptions import SubscriptionId


@dataclass
class BaseSubscriptionRepository(ABC):

    @abstractmethod
    async def create(self, subscription: Subscription) -> None: ...

    @abstractmethod
    async def deactivate(self, id: SubscriptionId) -> None: ...

    @abstractmethod
    async def activate(self, id: SubscriptionId) -> None: ...

    @abstractmethod
    async def get(self) -> list[Subscription]: ...

    @abstractmethod
    async def get_by_id(self, id: SubscriptionId) -> Subscription | None: ...