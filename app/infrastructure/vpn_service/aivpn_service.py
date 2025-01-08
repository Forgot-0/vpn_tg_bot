from dataclasses import dataclass
from datetime import datetime
from json import dumps
from typing import Any

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

    async def get_by_id(self, id: str, server: Server) -> ProfileDTO:
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

    async def create(self, id: str, subscription: Subscription, server: Server) -> str:
        cookies = await self.login(server=server)

        data = await self.get_by_id(id=id, server=server)
        url_vpn = self.get_vpn_uri(id=id, server=server)

        expiryTime = int((subscription.duration + datetime.now()).timestamp())*1000

        if data:

            if data.end_time >datetime.now():
                expiryTime = int((subscription.duration + data.end_time).timestamp())*1000
            url = server.update_by_id(id=id)

        else:
            url = server.url_create

        json = self.get_json_data(id=id, expiryTime=expiryTime, subscription=subscription)

        responce = await self.session.post(
            url=url,
            json=json,
            cookies=cookies
        )

        responce = await responce.json()
        if responce['success']:
            return url_vpn

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

    def get_vpn_uri(self, id: str, server: Server) -> str:
        return (
            f"vless://{id}@{server.ip}:{server.port}?security=reality&sni=google.com&fp=chrome&pbk={server.pbk}&"
            f"sid={server.short_id}&spx=%2F&type=tcp&flow=xtls-rprx-vision#{server.name}-{str(id)}"
        )

    def get_json_data(self, id: str, expiryTime: int, subscription: Subscription) -> dict[str, Any]: 
        return {
                'id': 1,
                'settings': dumps({
                    "clients": [
                        {
                            "id": str(id),
                            "flow": "xtls-rprx-vision",
                            "email": str(id),
                            "expiryTime": expiryTime,
                            "limitIp": subscription.limit_ip,
                            "totalGB": subscription.limit_trafic,
                            "enable": True,
                        }
                    ]
                })
            }
