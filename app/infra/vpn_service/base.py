from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities.server import Server
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.vpn_service.schema import Client, CreateVpnUrl



@dataclass(kw_only=True)
class BaseVpnService(ABC):

    username: str
    password: str
    secret: str

    @abstractmethod
    async def create(self, event: PaidSubscriptionEvent, server: Server) -> str:
        ...

    @abstractmethod
    async def login(self) -> None:
        ...

    @abstractmethod
    def get_vpn_uri(self, event: PaidSubscriptionEvent, server: Server) -> str:
        ...

    @abstractmethod
    async def delete_not_active(self, server: Server) -> None:
        ...

    @abstractmethod
    async def get_list(self, server: Server) -> dict[str, Any]:
        ...