from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.subscription import Subscription
from app.domain.entities.subscription_plan import SubscriptionPlan
from app.domain.values.subscriptions import SubscriptionStatus


class SubscriptionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None: ...
 
    @abstractmethod
    async def add(self, subscription: Subscription) -> None: ...
 
    @abstractmethod
    async def update(self, subscription: Subscription) -> None: ...
 
    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Subscription]: ...
 
    @abstractmethod
    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]: ...
 
    @abstractmethod
    async def list_expiring_within(self, days: int) -> list[Subscription]: ...

    @abstractmethod
    async def get_by_payment_order(self, payment_order_id: UUID) -> Subscription | None: ...
 
    @abstractmethod
    async def list_traffic_exceeded(self) -> list[Subscription]: ...
 


class SubscriptionPlanRepository(ABC):
    @abstractmethod
    async def get_by_id(self, plan_id: UUID) -> SubscriptionPlan | None: ...
 
    @abstractmethod
    async def get_by_code(self, code: str) -> SubscriptionPlan | None: ...
 
    @abstractmethod
    async def add(self, plan: SubscriptionPlan) -> None: ...
 
    @abstractmethod
    async def update(self, plan: SubscriptionPlan) -> None: ...
 
    @abstractmethod
    async def list_public_active(self) -> list[SubscriptionPlan]: ...
