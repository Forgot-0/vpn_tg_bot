from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Type

from app.domain.entities.server import VPNServer
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import PanelType, ProtocolCode
from app.domain.values.subscriptions import AccessArtifact


class ApiClient(ABC):
    @abstractmethod
    async def create_or_upgrade_subscription(
        self, subscription: Subscription, server: VPNServer
    ) -> None: ...

    @abstractmethod
    async def get_protocols(self, server: VPNServer)  -> dict[ProtocolCode, dict[str, Any]]: ...

    @abstractmethod
    async def get_subscription_info(self, server: VPNServer) -> AccessArtifact | None: ...

    @abstractmethod
    async def get_configs_vpn(
        self, subscription: Subscription, server: VPNServer
    ) -> dict[ProtocolCode, dict[str, Any]]: ...

    @abstractmethod
    async def delete_inactive_clients(self, server: VPNServer) -> None: ...

    @abstractmethod
    async def delete_client(self, subscription: Subscription, server: VPNServer) -> None: ...



@dataclass
class ApiClientFactory(ApiClient):
    _registry: dict[PanelType, ApiClient] = field(default_factory=dict)

    def register(self, api_type: PanelType, api_client: ApiClient) -> None:
        self._registry[api_type] = api_client

    def get(self, api_type: PanelType) -> ApiClient:
        api_client = self._registry.get(api_type)
        if api_client is None:
            raise
        return api_client

    async def create_or_upgrade_subscription(
        self,
        subscription: Subscription,
        server: VPNServer
    ) -> None:
        api_client = self.get(server.panel_type)
        await api_client.create_or_upgrade_subscription(
            subscription=subscription, server=server
        )

    async def get_protocols(self, server: VPNServer) -> dict[ProtocolCode, dict[str, Any]]:
        api_client = self.get(server.panel_type)
        return await api_client.get_protocols(server=server)

    async def delete_inactive_clients(self, server: VPNServer) -> None:
        api_client = self.get(server.panel_type)
        await api_client.delete_inactive_clients(server=server)

    async def delete_client(self, subscription: Subscription, server: VPNServer) -> None:
        api_client = self.get(server.panel_type)
        await api_client.delete_client(subscription=subscription, server=server)

    async def get_configs_vpn(
            self, subscription: Subscription, server: VPNServer
        )  -> dict[ProtocolCode, dict[str, Any]]:

        api_client = self.get(server.panel_type)
        return await api_client.get_configs_vpn(subscription=subscription, server=server)

    async def get_subscription_info(self, server: VPNServer) -> AccessArtifact | None:
        api_client = self.get(server.panel_type)
        return await api_client.get_subscription_info(server=server)


@dataclass
class ProtocolBuilder(ABC):

    @abstractmethod
    def build_params(self, subscription: Subscription, server: VPNServer) -> dict[str, Any]: ...

    @abstractmethod
    def build_config_vpn(
        self, subscription: Subscription, server: VPNServer
    ) -> dict[ProtocolCode, dict[str, Any]]: ...

    @abstractmethod
    def build_config(self, data: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class ProtocolBuilderFactory:
    _registry: dict[tuple[PanelType, ProtocolCode], Type[ProtocolBuilder]] = field(default_factory=dict)

    def register(
            self,
            api_type: PanelType,
            protocol_type: ProtocolCode,
            builder: Type[ProtocolBuilder]
        ) -> None:
        self._registry[(api_type, protocol_type)] = builder

    def get(self, api_type: PanelType, protocol_type: ProtocolCode) -> ProtocolBuilder:
        key = (api_type, protocol_type)

        if key not in self._registry:
            raise

        builder_cls = self._registry[key]

        return builder_cls()
