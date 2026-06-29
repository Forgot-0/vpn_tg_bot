from __future__ import annotations
from dataclasses import dataclass, field

from app.application.interfaces.panel.panel_provider import PanelProviderPort
from app.domain.entities.server import VPNServer
from app.domain.errors import PanelClientNotRegisteredError
from app.domain.values.servers import PanelType

@dataclass
class PanelRegistry:
    providers: dict[PanelType, PanelProviderPort] = field(default_factory=dict)

    def register(self, provider: PanelProviderPort) -> None:
        self.providers[provider.panel_type] = provider

    def get(self, panel_type: PanelType) -> PanelProviderPort:
        provider = self.providers.get(panel_type)
        if provider is None:
            raise PanelClientNotRegisteredError()

        return provider

    def get_for_server(self, server: VPNServer) -> PanelProviderPort:
        return self.get(server.panel_type)
