from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.plan import SubscriptionPlan


class PlanRepository(ABC):

    @abstractmethod
    async def get_by_id(self, plan_id: UUID) -> SubscriptionPlan | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> SubscriptionPlan | None: ...

    @abstractmethod
    async def list_public(self) -> list[SubscriptionPlan]: ...

    @abstractmethod
    async def list_all(self) -> list[SubscriptionPlan]: ...

    @abstractmethod
    async def add(self, plan: SubscriptionPlan) -> None: ...

    @abstractmethod
    async def update(self, plan: SubscriptionPlan) -> None: ...
