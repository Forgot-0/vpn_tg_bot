from domain.entities.user import User
from domain.entities.subscription import Subscription
from domain.entities.server import Server
from domain.values.servers import ProtocolType, VPNConfig
from domain.services.ports import BaseApiClient

class MockApiClient(BaseApiClient):
    async def create_subscription(self, user: User, subscription: Subscription, server: Server) -> list[VPNConfig]:
        dummy_config = VPNConfig(
            protocol_type=ProtocolType.mock,
            config="dummy_config"
        )
        return [dummy_config]

    async def delete_inactive_clients(self) -> None:
        return

    async def upgrade_client(self, user: User, subscription: Subscription, server: Server) -> None:
        return