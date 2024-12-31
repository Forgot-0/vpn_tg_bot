from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from application.dto.profile import ProfileDTO
from domain.entities.server import Server
from domain.entities.subscription import Subscription




@dataclass(kw_only=True)
class BaseVpnService(ABC):

    username: str
    password: str
    secret: str

    @abstractmethod
    async def create(self, id: str, subscription: Subscription, server: Server) -> str: ...

    @abstractmethod
    async def login(self) -> None: ...

    @abstractmethod
    def get_vpn_uri(self, id: str, server: Server) -> str: ...

    @abstractmethod
    async def delete_not_active(self, server: Server) -> None: ...

    @abstractmethod
    async def get_list(self, server: Server) -> dict[str, Any]: ...

    @abstractmethod
    async def get_by_id(self, id: str, server: Server) -> ProfileDTO: ...

    # @abstractmethod
    # async def update(id: str, server: Server, new_data: dict[str, Any]) -> None: ...