from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.server import VPNServer


class VPNServerRepository(ABC):
    @abstractmethod
    async def get_by_id(self, server_id: UUID) -> VPNServer | None: ...

    @abstractmethod
    async def add(self, server: VPNServer) -> None: ...

    @abstractmethod
    async def update(self, server: VPNServer) -> None: ...

    @abstractmethod
    async def delete(self, server_id: UUID) -> None: ...

    @abstractmethod
    async def list_active(self) -> list[VPNServer]: ...

    @abstractmethod
    async def list_by_region(self, region_code: str) -> list[VPNServer]: ...

    @abstractmethod
    async def get_max_free_server(
        self,
        protocols: frozenset[str],
        features: frozenset[str],
    ) -> VPNServer | None: ...
