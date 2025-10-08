from domain.entities.user import User
from domain.entities.subscription import Subscription
from domain.entities.server import Server
from domain.services.ports import BaseApiClient
from domain.values.servers import ProtocolConfig, ProtocolType, VPNConfig

class MockApiClient(BaseApiClient):
    def __init__(self) -> None:
        self.data = {}

    async def create_or_upgrade_subscription(
            self, user: User, subscription: Subscription,
            server: Server
        ) -> list[VPNConfig]:
        dummy_config = VPNConfig(
            protocol_type=ProtocolType.mock,
            config="dummy_config"
        )
        key = (user.id, subscription.id, server.id)
        self.data[key] = dummy_config
        return [dummy_config]

    async def delete_inactive_clients(self, server: Server) -> None:
        ...

    async def delete_client(self, user: User, subscription: Subscription, server: Server) -> None:
        key = (user.id, subscription.id, server.id)
        self.data.pop(key)

    async def get_configs(self, server: Server) -> list[ProtocolConfig]:
        return [ProtocolConfig({}, protocol_type=ProtocolType.mock)]