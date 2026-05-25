from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal

from app.domain.entities.server import VPNServer
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import PanelType
from app.domain.values.subscriptions import AccessCredential


class PanelClient(ABC):

    @property
    @abstractmethod
    def panel_type(self) -> PanelType: ...

    @abstractmethod
    async def create(
        self,
        server: VPNServer,
        subscription: Subscription,
    ) -> list[AccessCredential]:
        ...

    @abstractmethod
    async def delete(
        self,
        server: VPNServer,
        subscription: Subscription,
    ) -> None:
        ...

    @abstractmethod
    async def sync_traffic(
        self,
        server: VPNServer,
        subscription: Subscription,
    ) -> Decimal:
        ...


@dataclass
class PanelClientFactory:
    _clients: dict[PanelType, PanelClient] = field(default_factory=dict, init=False)

    def register(self, client: PanelClient) -> None:
        self._clients[client.panel_type] = client

    def get_client(self, server: VPNServer) -> PanelClient:
        client = self._clients.get(server.panel_type)
        if client is None:
            raise 
        return client

