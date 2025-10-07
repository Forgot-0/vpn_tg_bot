from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.values.servers import ProtocolConfig, ProtocolType, VPNConfig



class BaseApiClient(ABC):
    @abstractmethod
    async def create_or_upgrade_subscription(
        self,user: User,
        subscription: Subscription,
        server: Server) -> None: ...

    @abstractmethod
    async def get_configs(self, server: Server)  -> list[ProtocolConfig]: ...

    @abstractmethod
    async def delete_inactive_clients(self, server: Server) -> None: ...

    @abstractmethod
    async def delete_client(self, user: User, subscription: Subscription, server: Server) -> None: ...

@dataclass
class BaseProtocolBuilder(ABC):
    protocol_type: ProtocolType

    @abstractmethod
    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]: ...

    @abstractmethod
    def builde_config_vpn(self, user: User, subscription: Subscription, server: Server) -> VPNConfig: ...

    @abstractmethod
    def build_config(self, data: dict[str, Any]) -> dict[str, Any]: ...