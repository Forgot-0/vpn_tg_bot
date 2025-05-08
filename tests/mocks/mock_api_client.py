from domain.entities.user import User
from domain.entities.subscription import Subscription
from domain.entities.server import Server
from domain.services.ports import BaseApiClient
from domain.values.servers import ProtocolType, VPNConfig

class MockApiClient(BaseApiClient):
    def __init__(self) -> None:
        self.data = {}

    async def create_subscription(self, user: User, subscription: Subscription, server: Server) -> list[VPNConfig]:
        dummy_config = VPNConfig(
            protocol_type=ProtocolType.mock,
            config="dummy_config"
        )
        key = (user.id, subscription.id, server.id)
        self.data[key] = dummy_config
        return [dummy_config]

    async def delete_inactive_clients(self, user: User, subscription: Subscription, server: Server) -> None:
        key = (user.id, subscription.id, server.id)
        self.data.pop(key)

    async def upgrade_client(self, user: User, subscription: Subscription, server: Server) -> None:
        return