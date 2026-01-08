
from dataclasses import dataclass, field
from app.domain.entities.server import Server
from app.domain.entities.subscription import Subscription
from app.domain.entities.user import User
from app.domain.services.ports import BaseApiClient
from app.domain.values.servers import ApiType, ProtocolConfig, SubscriptionConfig, VPNConfig


@dataclass
class ApiClientRouter(BaseApiClient):
    _registry: dict[ApiType, BaseApiClient] = field(default_factory=dict)

    def register(self, api_type: ApiType, api_client: BaseApiClient) -> None:
        self._registry[api_type] = api_client

    def get(self, api_type: ApiType) -> BaseApiClient:
        api_client = self._registry.get(api_type)
        if api_client is None:
            raise
        return api_client

    async def create_or_upgrade_subscription(
        self, user: User,
        subscription: Subscription,
        server: Server
    ) -> None:
        api_client = self.get(server.api_type)
        await api_client.create_or_upgrade_subscription(
            user=user, subscription=subscription, server=server
        )

    async def get_protocols(self, server: Server)  -> list[ProtocolConfig]:
        api_client = self.get(server.api_type)
        return await api_client.get_protocols(server=server)

    async def delete_inactive_clients(self, server: Server) -> None:
        api_client = self.get(server.api_type)
        await api_client.delete_inactive_clients(server=server)

    async def delete_client(self, user: User, subscription: Subscription, server: Server) -> None:
        api_client = self.get(server.api_type)
        await api_client.delete_client(user=user, subscription=subscription, server=server)

    async def get_configs_vpn(self, user: User, subscription: Subscription, server: Server) -> list[VPNConfig]:
        api_client = self.get(server.api_type)
        return await api_client.get_configs_vpn(user=user, subscription=subscription, server=server)

    async def get_subscription_info(self, server: Server) -> SubscriptionConfig | None:
        api_client = self.get(server.api_type)
        return await api_client.get_subscription_info(server=server)
