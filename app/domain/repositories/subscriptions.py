from abc import abstractmethod
from dataclasses import dataclass

from app.domain.entities.subscription import Subscription
from app.domain.repositories.base import BaseRepository
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId


@dataclass
class BaseSubscriptionRepository(BaseRepository[Subscription]):

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

    @abstractmethod
    async def get_by_user(self, user_id: UserId) -> list[Subscription]: ...

    @abstractmethod
    async def update(self, subscription: Subscription) -> None: ...

