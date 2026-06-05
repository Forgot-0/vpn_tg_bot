from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.plan import Plan


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
