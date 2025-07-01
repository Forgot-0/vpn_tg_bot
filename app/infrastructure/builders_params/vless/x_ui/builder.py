from dataclasses import dataclass
import json
from typing import Any

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseProtocolBuilder
from domain.values.servers import ProtocolType, VPNConfig


@dataclass
class Vless3XUIProtocolBuilder(BaseProtocolBuilder):

    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]:
        return {
            "id": server.get_config_by_protocol(self.protocol_type).config['inbound_id'],
            "settings": json.dumps({
                "clients": [
                    {
                        "id": str(subscription.id.value.hex),
                        "flow": server.get_config_by_protocol(self.protocol_type).config["flow"],
                        "email": str(subscription.id.value.hex),
                        "expiryTime": int(subscription.end_date.timestamp()*1000),
                        "limitIp": subscription.device_count,
                        "totalGB": 0,
                        "enable": True,
                    }
                ]
            })
        }

    def builde_config_vpn(self, user: User, subscription: Subscription, server: Server) -> VPNConfig:
        return VPNConfig(
            protocol_type=self.protocol_type,
            config=(
                "vless://{id}@{ip}:{port}?security={security}&sni={sni}&fp={fp}&pbk={pbk}&"
                "sid={short_id}&spx={spx}&type=tcp&flow={flow}#{name}-{id}"
            ).format(
                **server.get_config_by_protocol(self.protocol_type).config,
                ip=server.api_config["ip"],
                id=subscription.id.value.hex
                )
        )

