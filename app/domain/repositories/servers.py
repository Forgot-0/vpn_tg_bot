from abc import abstractmethod
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.server import VPNServer
from app.domain.repositories.base import Repository
from app.domain.values.subscriptions import VPNProtocol


class VPNServerRepository(Repository[VPNServer, UUID]):
    @abstractmethod
    async def get_by_id(self, server_id: UUID) -> VPNServer | None:
        ...

    @abstractmethod
    async def add(self, entity: VPNServer) -> None:
        ...

    @abstractmethod
    async def update(self, server_entity: VPNServer) -> None:
        ...

    @abstractmethod
    async def delete(self, server_id: str) -> None:
        ...

    @abstractmethod
    async def list_active(self) -> list[VPNServer]:
        ...

    @abstractmethod
    async def list_by_region(self, region_code: str) -> list[VPNServer]:
        ...

    @abstractmethod
    async def find_supporting(
        self, protocols: FrozenSet[VPNProtocol]
    ) -> list[VPNServer]:
        ...