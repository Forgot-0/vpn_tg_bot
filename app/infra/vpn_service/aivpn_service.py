from dataclasses import dataclass
from json import dumps
from typing import Any
from uuid import UUID

from aiohttp import ClientSession
from domain.entities.server import Server
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.vpn_service.base import BaseVpnService
from infra.vpn_service.convertors import convert_from_event_to_creat_client
from infra.vpn_service.schema import Client, CreateVpnUrl


@dataclass
class AIVpnService(BaseVpnService):
    session: ClientSession

    async def login(self, server: Server):
        responce = await self.session.post(
            url=server.uri_login,
            data={
                'username': self.username,
                'password': self.password,
                'loginSecret': self.secret
            }
        )
        return responce.cookies

    async def create(self, user_id: UUID, event: PaidSubscriptionEvent, server: Server) -> str | None:
        cookies = await self.login(server=server)
        json = convert_from_event_to_creat_client(
            user_id=user_id,
            event=event
        )

        url = self.get_vpn_uri(user_id=user_id, tg_id=event.tg_id, server=server)

        responce = await self.session.post(
            url=server.uri_create,
            json=json,
            cookies=cookies
        )

        responce = await responce.json()
        if responce['success']:
            return url

    async def udate(self, data: dict[str, Any]) -> None:
        # data = data.model_dump()
        # await self.session.post(
        #     url=f'{self.uri_update}/{data['id']}',
        #     data=data
        # )
        ...

    async def get_by_id(self, id: str, server: Server) -> Client | None:
        # data = await (await self.session.get(url=f"{self.uri_get}/{id}")).json()

        # if data['success']:
        #     return Client(**data['obj'][0])
        ...

    def get_vpn_uri(self, user_id: UUID, tg_id: int, server: Server) -> str:
        return f"""vless://{user_id}@{server.ip}:443?security=reality&sni=google.com&fp=chrome&pbk={server.pbk}&sid=ce352f&spx=/&type=tcp&flow=xtls-rprx-vision&encryption=none#VLESS%20%D1%81%20XTLS-Reality-{tg_id}"""
    
    