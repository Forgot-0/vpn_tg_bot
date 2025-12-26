
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.base import PaginatedResult
from app.application.dtos.servers.base import ServerListParams
from app.domain.entities.server import Server
from app.domain.values.servers import ProtocolType


@dataclass
class BaseServerRepository(ABC):

    @abstractmethod
    async def get_by_max_free(self, type_protocols: list[ProtocolType]) -> Server | None: ...

    @abstractmethod
    async def create(self, server: Server) -> None: ...

    @abstractmethod
    async def update_decrement_free(self, server_id: UUID, decr: int = -1) -> None: ...

    @abstractmethod
    async def get_all(self) -> list[Server]: ...

    @abstractmethod
    async def get_all_protocols(self) -> list[str]: ...

    @abstractmethod
    async def get_by_id(self, server_id: UUID) -> Server | None: ...

    @abstractmethod
    async def set_free(self, server_id: UUID, new_free: int) -> None: ...

    @abstractmethod
    async def get_list(self, filter_params: ServerListParams) -> PaginatedResult[Server]: ...

    @abstractmethod
    async def delete_by_id(self, server_id: UUID) -> None: ...
