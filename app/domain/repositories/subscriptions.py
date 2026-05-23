from abc import abstractmethod

from app.domain.entities.subscription import Subscription, SubscriptionPlan
from app.domain.repositories.base import Repository
from app.domain.values.subscriptions import SubscriptionStatus
from app.domain.values.users import UserId


class SubscriptionRepository(Repository[Subscription, str]):
    @abstractmethod
    async def list_by_user(self, user_id: UserId) -> list[Subscription]: ...

    @abstractmethod
    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]: ...

    @abstractmethod
    async def list_expiring(self, within_days: int) -> list[Subscription]: ...


class SubscriptionPlanRepository(Repository[SubscriptionPlan, str]):
    @abstractmethod
    async def get_by_code(self, code: str) -> SubscriptionPlan | None: ...

    @abstractmethod
    async def list_active(self) -> list[SubscriptionPlan]: ...
