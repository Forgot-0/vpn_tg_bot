from dataclasses import dataclass
import json
from typing import Any

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseProtocolBuilder
from domain.values.servers import VPNConfig
from infrastructure.api_client.x_ui.schema import Inbound


@dataclass
class Vless3XUIProtocolBuilder(BaseProtocolBuilder):

    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]:
        return {
            "id": server.get_config_by_protocol(self.protocol_type).config['id'],
            "settings": json.dumps({
                "clients": [
                    {
                        "id": subscription.id.as_generic_type(),
                        "flow": "xtls-rprx-vision",
                        "email": subscription.id.as_generic_type(),
                        "expiryTime": int(subscription.end_date.timestamp()*1000),
                        "limitIp": subscription.device_count,
                        "totalGB": 0,
                        "enable": True,
                    }
                ]
            })
        }

    def builde_config_vpn(self, user: User, subscription: Subscription, server: Server) -> VPNConfig:
        config = server.get_config_by_protocol(self.protocol_type).config
        return VPNConfig(
            protocol_type=self.protocol_type,
            config=Inbound.from_json(config).gen_vless_link(
                address=server.api_config.domain if server.api_config.domain else server.api_config.ip,
                client_id=subscription.id.as_generic_type(),
                flow="xtls-rprx-vision",
                remark=f"{subscription.id.as_generic_type()}"
            )
        )

    def build_config(self, data: dict[str, Any]) -> dict[str, Any]:
        data['settings'] = json.loads(data['settings'])
        data['streamSettings'] = (json.loads(data['streamSettings']))
        data['sniffing'] = json.loads(data['sniffing'])

        return data