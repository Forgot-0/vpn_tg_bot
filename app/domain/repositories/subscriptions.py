from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.subscription import Subscription
from app.domain.entities.plan import Plan
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
    async def get_by_payment_intent(self, payment_intent_id: UUID) -> Subscription | None: ...
 
    @abstractmethod
    async def list_traffic_exceeded(self) -> list[Subscription]: ...
 


class PlanRepository(ABC):
    @abstractmethod
    async def get_by_id(self, plan_id: UUID) -> Plan | None: ...
 
    @abstractmethod
    async def get_by_code(self, code: str) -> Plan | None: ...
 
    @abstractmethod
    async def add(self, plan: Plan) -> None: ...
 
    @abstractmethod
    async def update(self, plan: Plan) -> None: ...
 
    @abstractmethod
    async def list_public_active(self) -> list[Plan]: ...
