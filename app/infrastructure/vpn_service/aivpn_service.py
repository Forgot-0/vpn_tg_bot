from dataclasses import dataclass
from datetime import datetime
from json import dumps
from typing import Any
from uuid import UUID

from aiohttp import ClientSession
from application.dto.profile import ProfileDTO
from domain.entities.server import Server
from domain.entities.subscription import Subscription
from infrastructure.vpn_service.base import BaseVpnService


@dataclass
class AIVpnService(BaseVpnService):
    session: ClientSession

    async def login(self, server: Server):
        responce = await self.session.post(
            url=server.url_login,
            data={
                'username': self.username,
                'password': self.password,
                'loginSecret': self.secret
            }
        )
        return responce.cookies

    async def get_by_id(self, id: UUID, server: Server) -> ProfileDTO:
        cookies = await self.login(server=server)

        responce = await self.session.get(
            url=server.get_by_id(id=id),
            cookies=cookies
        )

        responce = await responce.json()
        data = responce['obj']

        if len(data) > 0:
            data = data[0]
            data['vpn_url'] = self.get_vpn_uri(id=id, server=server)
            return ProfileDTO.from_dict(data)
        return None

    async def create(self, order_id: UUID, subscription: Subscription, server: Server) -> str:
        cookies = await self.login(server=server)

        expiryTime = int(
            (
                subscription.duration + datetime.now()
            ).timestamp())*1000 if subscription.duration.total_seconds() != 0 else 0

        json = {
                'id': 1,
                'settings': dumps({
                    "clients": [
                        {
                            "id": str(order_id),
                            "flow": "xtls-rprx-vision",
                            "email": str(order_id),
                            "expiryTime": expiryTime,
                            "limitIp": subscription.limit_ip,
                            "totalGB": subscription.limit_trafic,
                            "enable": True,
                        }
                    ]
                })
            }

        url = self.get_vpn_uri(id=order_id, server=server)

        responce = await self.session.post(
            url=server.url_create,
            json=json,
            cookies=cookies
        )

        responce = await responce.json()
        if responce['success']:
            return url

        raise

    async def delete_not_active(self, server: Server) -> None:
        cookies = await self.login(server=server)
        await self.session.post(
            url=server.url_delete_not_active,
            cookies=cookies
        )

    async def get_list(self, server: Server) -> dict[str, Any]:
        cookies = await self.login(server=server)
        responce = await self.session.get(
            url=server.url_list,
            cookies=cookies
        )
        return await responce.json()

    def get_vpn_uri(self, id: UUID, server: Server) -> str:
        return (
            f"vless://{id}@{server.ip}:{server.port}?security=reality&sni=google.com&fp=chrome&pbk={server.pbk}&"
            f"sid=ce352f&spx=/&type=tcp&flow=xtls-rprx-vision&encryption=none#{server.name}-{str(id)}"
        )