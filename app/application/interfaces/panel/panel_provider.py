from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

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
        email: str,
        traffic_limit_bytes: int | None,
        expire_timestamp_ms: int | None,
        device_limit: int | None,
        inbound_ids: list[int],
        protocols: frozenset[ProtocolCode],
    ) -> ProvisionedClientInfo: ...

    @abstractmethod
    async def update_client(
        self,
        panel_client_id: str,
        *,
        traffic_limit_bytes: int | None = None,
        expire_timestamp_ms: int | None = None,
        device_limit: int | None = None,
        enable: bool | None = None,
    ) -> None: ...

    @abstractmethod
    async def delete_client(self, panel_client_id: str) -> None: ...

    @abstractmethod
    async def get_client_traffic(self, panel_client_id: str) -> ClientTrafficInfo: ...

    @abstractmethod
    async def reset_client_traffic(self, panel_client_id: str) -> None: ...

    @abstractmethod
    async def get_subscription_url(self, panel_client_id: str) -> str: ...

