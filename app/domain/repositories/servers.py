
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.server import Server


@dataclass
class BaseServerRepository(ABC):

    @abstractmethod
    async def get_by_max_free(self) -> Server | None: ...

    @abstractmethod
    async def create(self, server: Server) -> None: ...

    @abstractmethod
    async def update_decrement_free(self, server_id: UUID, decr: int = -1) -> None: ...

    @abstractmethod
    async def get_all(self) -> list[Server]: ...

    @abstractmethod
    async def get_by_id(self, server_id: UUID) -> Server | None: ...

    @abstractmethod
    async def set_free(self, server_id: UUID, new_free: int) -> None: ...
