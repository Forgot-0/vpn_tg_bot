from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from app.domain.entities.access import ProvisionedAccess
from app.domain.entities.server import PanelConnection, VPNServer
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import FeatureCode, PanelType, ProtocolCode


@dataclass(frozen=True)
class PanelServerInfoResult:
    supported_protocols: frozenset[ProtocolCode]
    supported_features: frozenset[FeatureCode] = frozenset()
    panel_config: dict[str, object] = field(default_factory=dict)
    current_clients: int = 0


class PanelClient(ABC):
    @property
    @abstractmethod
    def panel_type(self) -> PanelType: ...

    @abstractmethod
    async def create(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> ProvisionedAccess: ...

    @abstractmethod
    async def delete(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> None: ...

    @abstractmethod
    async def sync_traffic(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> Decimal: ...

    @abstractmethod
    async def get_info(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
    ) -> PanelServerInfoResult: ...


@dataclass
class PanelClientFactory:
    _clients: dict[PanelType, PanelClient] = field(default_factory=dict, init=False)

    def register(self, client: PanelClient) -> None:
        self._clients[client.panel_type] = client

    def get_client(self, connection: PanelConnection) -> PanelClient:
        client = self._clients.get(connection.panel_type)
        if client is None:
            raise
        return client