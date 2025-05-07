from typing import Any
from domain.entities.user import User
from domain.entities.subscription import Subscription
from domain.entities.server import Server
from domain.services.ports import BaseProtocolBuilder
from domain.values.servers import ProtocolType, VPNConfig

class MockProtocolBuilder(BaseProtocolBuilder):
    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]:
        return {"dummy_param": "value"}

    def builde_config_vpn(self, user: User, subscription: Subscription, server: Server) -> VPNConfig:
        return VPNConfig(
            protocol_type=ProtocolType.mock,
            config="dummy_config"
        )