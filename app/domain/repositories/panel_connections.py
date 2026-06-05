from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.server import PanelConnection, VPNServer

class PanelConnectionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, connection_id: UUID) -> PanelConnection | None: ...

    @abstractmethod
    async def get_by_server(self, server_id: UUID) -> PanelConnection | None: ...

    @abstractmethod
    async def list_active(self) -> list[PanelConnection]: ...

    @abstractmethod
    async def add(self, connection: PanelConnection) -> None: ...

    @abstractmethod
    async def update(self, connection: PanelConnection) -> None: ...

    @abstractmethod
    async def delete(self, connection_id: UUID) -> None: ...
