from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.server import VPNServer
from app.domain.values.servers import FeatureCode, ProtocolCode


class ServerRepository(ABC):

    @abstractmethod
    async def get_by_id(self, server_id: UUID) -> VPNServer | None: ...

    @abstractmethod
    async def list_active(self) -> list[VPNServer]: ...

    @abstractmethod
    async def list_capable(
        self,
        *,
        protocols: frozenset[ProtocolCode],
        features: frozenset[FeatureCode],
    ) -> list[VPNServer]: ...

    @abstractmethod
    async def add(self, server: VPNServer) -> None: ...

    @abstractmethod
    async def update(self, server: VPNServer) -> None: ...
