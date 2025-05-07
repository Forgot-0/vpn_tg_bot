from typing import List, Optional
from uuid import UUID
from domain.entities.server import Server
from domain.repositories.servers import BaseServerRepository


class MockServerRepository(BaseServerRepository):
    def __init__(self):
        self._data: dict[UUID, Server] = {}

    async def get_by_max_free(self) -> Optional[Server]:
        if not self._data:
            return None
        return max(self._data.values(), key=lambda server: server.free)

    async def create(self, server: Server) -> None:
        self._data[server.id] = server

    async def update_decrement_free(self, server_id: UUID) -> None:
        if server_id in self._data:
            server = self._data[server_id]
            server.free = max(0, server.free - 1)
            self._data[server_id] = server

    async def get_all(self) -> List[Server]:
        return list(self._data.values())

    async def get_by_id(self, server_id: UUID) -> Optional[Server]:
        return self._data.get(server_id)

    async def set_free(self, server_id: UUID, new_free: int) -> None:
        if server_id in self._data:
            server = self._data[server_id]
            server.free = new_free
            self._data[server_id] = server