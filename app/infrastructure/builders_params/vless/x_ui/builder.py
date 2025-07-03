from dataclasses import dataclass
import json
from typing import Any

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseProtocolBuilder
from domain.values.servers import VPNConfig


@dataclass
class Vless3XUIProtocolBuilder(BaseProtocolBuilder):

    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]:
        return {
            "id": server.get_config_by_protocol(self.protocol_type).config['inbound_id'],
            "settings": json.dumps({
                "clients": [
                    {
                        "id": subscription.id.as_generic_type(),
                        "flow": server.get_config_by_protocol(self.protocol_type).config["flow"],
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
            config=(
                "vless://{id}@{ip}:{port}?security={security}&sni={sni}&fp={fp}&pbk={pbk}&"
                "sid={sid}&spx={spx}&type=tcp&flow=xtls-rprx-vision#{name}-{id}"
            ).format(
                **config,
                ip=server.api_config["ip"],
                id=subscription.id.as_generic_type()
                )
        )

    def build_config(self, data: dict[str, Any]) -> dict[str, Any]:
        vpn_config = {}

        vpn_config['port'] = data['port']
        vpn_config['inbound_id'] = data['id']
        config = json.loads(data['streamSettings'])
        vpn_config['security'] = config['security']
        if 'realitySettings' in config:
            vpn_config['sid'] = config['realitySettings']['shortIds'][0]
            vpn_config['pbk'] = config['realitySettings']['settings']['publicKey']
            vpn_config['fp'] = config['realitySettings']['settings']['fingerprint']
            vpn_config['spx'] = config['realitySettings']['settings']['spiderX']
            vpn_config['sni'] = config['realitySettings']['serverNames'][0]

        return vpn_config