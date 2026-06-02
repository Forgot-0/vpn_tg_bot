from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.access import ProvisionedAccess


class ProvisionedAccessRepository(ABC):
    @abstractmethod
    async def get_by_id(self, access_id: UUID) -> ProvisionedAccess | None: ...

    @abstractmethod
    async def list_by_subscription(self, subscription_id: UUID) -> list[ProvisionedAccess]: ...

    @abstractmethod
    async def add(self, access: ProvisionedAccess) -> None: ...

    @abstractmethod
    async def update(self, access: ProvisionedAccess) -> None: ...
