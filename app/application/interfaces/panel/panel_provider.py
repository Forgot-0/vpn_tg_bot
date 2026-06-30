from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.server import VPNServer
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import PanelType, ProtocolCode


@dataclass(frozen=True)
class ProvisionedClientInfo:
    panel_client_id: str
    subscription_url: str
    access_links: list[str]


@dataclass(frozen=True)
class ClientTrafficInfo:
    panel_client_id: str
    bytes_uploaded: int
    bytes_downloaded: int
    total_bytes: int
    is_enabled: bool


class PanelProviderPort(ABC):

    @property
    @abstractmethod
    def panel_type(self) -> PanelType: ...

    @abstractmethod
    async def create_client(
        self,
        *,
        subscription: Subscription,
        server: VPNServer,
    ) -> ProvisionedClientInfo: ...

    @abstractmethod
    async def update_client(
        self,
        *,
        subscription: Subscription,
        server: VPNServer,
    ) -> None: ...

    @abstractmethod
    async def delete_client(
        self,
        subscription: Subscription,
        server: VPNServer
    ) -> None: ...

    @abstractmethod
    async def get_client_traffic(
        self,
        subscription: Subscription,
        server: VPNServer
    ) -> ClientTrafficInfo: ...

    @abstractmethod
    async def reset_client_traffic(
        self,
        subscription: Subscription,
        server: VPNServer
    ) -> None: ...

    @abstractmethod
    async def get_subscription_url(
        self,
        subscription: Subscription,
        server: VPNServer
    ) -> str: ...

