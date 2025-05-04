from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User



class BaseApiClient(ABC):
    @abstractmethod
    async def create_subscription(self,user: User, subscription: Subscription, server: Server) -> None: ...

    @abstractmethod
    async def delete_inactive_clients(self) -> None: ...

    @abstractmethod
    async def upgrade_client(self, user: User, subscription: Subscription, server: Server) -> None:...


@dataclass
class BaseProtocolBuilder(ABC):
    config: dict[str, Any]

    @abstractmethod
    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]: ...
