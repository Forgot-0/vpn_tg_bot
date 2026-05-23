from abc import abstractmethod
from uuid import UUID

from app.domain.entities.subscription import Subscription, SubscriptionPlan
from app.domain.repositories.base import Repository
from app.domain.values.subscriptions import SubscriptionStatus


class SubscriptionRepository(Repository[Subscription, UUID]):
    @abstractmethod
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None:
        ...

    @abstractmethod
    async def add(self, entity: Subscription) -> None:
        ...

    @abstractmethod
    async def update(self, subscription_entity: Subscription) -> None:
        ...

    @abstractmethod
    async def delete(self, subscription_id: str) -> None:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Subscription]:
        ...

    @abstractmethod
    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]:
        ...

    @abstractmethod
    async def list_expiring(self, within_days: int) -> list[Subscription]:
        ...


class SubscriptionPlanRepository(Repository[SubscriptionPlan, UUID]):
    @abstractmethod
    async def get(self, subscription_plan_id: UUID) -> SubscriptionPlan | None:
        ...

    @abstractmethod
    async def add(self, subscription_plan_entity: SubscriptionPlan) -> None:
        ...

    @abstractmethod
    async def update(self, subscription_plan_entity: SubscriptionPlan) -> None:
        ...

    @abstractmethod
    async def delete(self, subscription_plan_id: UUID) -> None:
        ...

    @abstractmethod
    async def get_by_code(self, code: str) -> SubscriptionPlan | None:
        ...

    @abstractmethod
    async def list_active(self) -> list[SubscriptionPlan]:
        ...
