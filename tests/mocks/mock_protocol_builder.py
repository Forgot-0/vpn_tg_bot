from typing import Any
from app.domain.entities.user import User
from app.domain.entities.subscription import Subscription
from app.domain.entities.server import Server
from app.domain.services.ports import BaseProtocolBuilder
from app.domain.values.servers import ProtocolType, VPNConfig

class MockProtocolBuilder(BaseProtocolBuilder):
    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]:
        return {"dummy_param": "value"}

    def builde_config_vpn(self, user: User, subscription: Subscription, server: Server) -> VPNConfig:
        return VPNConfig(
            protocol_type=ProtocolType.mock,
            config="dummy_config"
        )

    def build_config(self, data: dict[str, Any]) -> dict[str, Any]:
        return {}