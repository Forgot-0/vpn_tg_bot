from dataclasses import dataclass
import json
from typing import Any

from app.domain.entities.server import Server
from app.domain.entities.subscription import Subscription
from app.domain.entities.user import User
from app.domain.services.ports import BaseProtocolBuilder
from app.domain.values.servers import VPNConfig
from app.infrastructure.api_client.x_ui.schema import Inbound


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
                        "subId": subscription.id.as_generic_type(),
                        "email": subscription.id.as_generic_type()+"vless",
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
        data['settings']['clients'] = []

        data['streamSettings'] = (json.loads(data['streamSettings']))
        data['sniffing'] = json.loads(data['sniffing'])
        data['clientStats'] = []

        return data