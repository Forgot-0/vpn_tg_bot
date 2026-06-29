from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.subscription import Subscription
from app.domain.values.subscriptions import SubscriptionStatus


class SubscriptionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Subscription]: ...

    @abstractmethod
    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]: ...

    @abstractmethod
    async def list_expiring_before(self, *, cutoff_days: int) -> list[Subscription]: ...

    @abstractmethod
    async def add(self, subscription: Subscription) -> None: ...

    @abstractmethod
    async def update(self, subscription: Subscription) -> None: ...
