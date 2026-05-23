from abc import abstractmethod
from typing import FrozenSet

from app.domain.entities.server import VPNServer
from app.domain.repositories.base import Repository
from app.domain.values.subscriptions import VPNProtocol


class VPNServerRepository(Repository[VPNServer, str]):
    @abstractmethod
    async def list_active(self) -> list[VPNServer]: ...

    @abstractmethod
    async def list_by_region(self, region_code: str) -> list[VPNServer]: ...

    @abstractmethod
    async def find_supporting(
        self, protocols: FrozenSet[VPNProtocol]
    ) -> list[VPNServer]: ...
