from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.dtos.servers import CreateClientCommand, PanelClientResult, TrafficStats
from app.domain.entities.server import VPNServer
from app.domain.values.servers import PanelType



class PanelPort(ABC):
    @property
    @abstractmethod
    def panel_type(self) -> PanelType:
        ...

    @abstractmethod
    async def create_client(
        self,
        server: VPNServer,
        command: CreateClientCommand,
    ) -> PanelClientResult:
        ...

    @abstractmethod
    async def update_client(
        self,
        server: VPNServer,
        panel_client_id: str,
        command: CreateClientCommand,
    ) -> PanelClientResult:
        ...

    @abstractmethod
    async def delete_client(
        self,
        server: VPNServer,
        panel_client_id: str,
    ) -> None:
        ...

    @abstractmethod
    async def get_traffic_stats(
        self,
        server: VPNServer,
        panel_client_id: str,
    ) -> TrafficStats:
        ...

    @abstractmethod
    async def reset_traffic(
        self,
        server: VPNServer,
        panel_client_id: str,
    ) -> None:
        ...

    @abstractmethod
    async def set_enabled(
        self,
        server: VPNServer,
        panel_client_id: str,
        *,
        enabled: bool,
    ) -> None:
        ...
