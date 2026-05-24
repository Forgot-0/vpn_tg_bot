from __future__ import annotations

from dataclasses import dataclass, field

from app.application.dtos.servers import CreateClientCommand, PanelClientResult, TrafficStats
from app.application.interfaces.servers import PanelPort
from app.domain.entities.server import VPNServer
from app.domain.values.servers import PanelType


@dataclass
class PanelGateway(PanelPort):
    ports: dict[PanelType, PanelPort] = field(default_factory=dict)

    @property
    def panel_type(self) -> PanelType:
        return PanelType.OTHER

    def _resolve(self, server: VPNServer) -> PanelPort:
        port = self.ports.get(server.panel_type)
        if port is None:
            raise 
        return port

    async def create_client(
        self,
        server: VPNServer,
        command: CreateClientCommand,
    ) -> PanelClientResult:
        return await self._resolve(server).create_client(server, command)

    async def update_client(
        self,
        server: VPNServer,
        panel_client_id: str,
        command: CreateClientCommand,
    ) -> PanelClientResult:
        return await self._resolve(server).update_client(server, panel_client_id, command)

    async def delete_client(
        self,
        server: VPNServer,
        panel_client_id: str,
    ) -> None:
        await self._resolve(server).delete_client(server, panel_client_id)

    async def get_traffic_stats(
        self,
        server: VPNServer,
        panel_client_id: str,
    ) -> TrafficStats:
        return await self._resolve(server).get_traffic_stats(server, panel_client_id)

    async def reset_traffic(
        self,
        server: VPNServer,
        panel_client_id: str,
    ) -> None:
        await self._resolve(server).reset_traffic(server, panel_client_id)

    async def set_enabled(
        self,
        server: VPNServer,
        panel_client_id: str,
        *,
        enabled: bool,
    ) -> None:
        await self._resolve(server).set_enabled(server, panel_client_id, enabled=enabled)
