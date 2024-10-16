from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession
from domain.entities.server import Server
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.vpn_service.base import BaseVpnService
from infra.vpn_service.convertors import convert_from_event_to_creat_client
from infra.vpn_service.schema import Client



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

    async def create(self, event: PaidSubscriptionEvent, server: Server) -> str:
        cookies = await self.login(server=server)

        json = convert_from_event_to_creat_client(
            event=event
        )

        url = self.get_vpn_uri(event=event, server=server)

        responce = await self.session.post(
            url=server.url_create,
            json=json,
            cookies=cookies
        )

        responce = await responce.json()
        if responce['success']:
            return url

        return 'Что то пошло не так обратитесь в службу поддержки'

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

    def get_vpn_uri(self, event: PaidSubscriptionEvent, server: Server) -> str:
        return f"""vless://{event.subscription_id}@{server.ip}:{server.port}?security=reality&sni=google.com&fp=chrome&pbk={server.pbk}&sid=ce352f&spx=/&type=tcp&flow=xtls-rprx-vision&encryption=none#{server.name}-{str(event.subscription_id)}"""