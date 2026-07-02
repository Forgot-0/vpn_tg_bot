from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.server import VPNServer
from app.domain.filters.base import BaseFilter
from app.domain.filters.condition import FilterOperator
from app.domain.repositories.filter import PageResult
from app.domain.values.servers import FeatureCode, PanelType, ProtocolCode



@dataclass
class ServerFilter(BaseFilter):
    name: str | None = None
    panel_type: PanelType = PanelType.X3UI

    def build_conditions(self) -> None:
        self.add_condition("name", FilterOperator.LIKE, self.name)

        self.add_condition("panel_type", FilterOperator.EQ, self.panel_type.value)



class ServerRepository(ABC):

    @abstractmethod
    async def get_by_id(self, server_id: UUID) -> VPNServer | None: ...

    @abstractmethod
    async def list_active(self) -> list[VPNServer]: ...

    @abstractmethod
    async def list_filtered(
        self,
        *,
        filter: ServerFilter
    ) -> PageResult[VPNServer]: ...

    @abstractmethod
    async def list_capable(
        self,
        *,
        protocols: frozenset[ProtocolCode],
        features: frozenset[FeatureCode],
    ) -> list[VPNServer]: ...

    @abstractmethod
    async def add(self, server: VPNServer, *, region_code: str | None = None) -> None: ...

    @abstractmethod
    async def update(self, server: VPNServer, *, region_code: str | None = None) -> None: ...

    @abstractmethod
    async def delete(self, server_id: UUID) -> None: ...
