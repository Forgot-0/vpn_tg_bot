from dataclasses import dataclass
from json import dumps

from aiohttp import ClientSession
from infra.vpn_service.base import BaseVpnService
from infra.vpn_service.schema import Client, CreateVpnUrl


@dataclass
class AIVpnService(BaseVpnService):
    session: ClientSession

    async def login(self):
        responce = await self.session.post(
            url=self.uri_login,
            data={
                'username': self.username,
                'password': self.password,
                'loginSecret': self.secret
            }
        )
        return responce.cookies

    async def create(self, data: CreateVpnUrl) -> str:
        cookies = await self.login()
        json = data.model_dump()

        url = self.get_vpn_urn(data=json)

        json['settings'] = dumps(json['settings'])
        responce = await self.session.post(
            url=self.uri_create,
            json=json,
            cookies=cookies
        )

        responce = await responce.json()
        if responce['success']:
            return url
        else:
            raise

    async def udate(self, data: Client) -> None:
        data = data.model_dump()
        await self.session.post(
            url=f'{self.uri_update}/{data['id']}',
            data=data
        )

    async def get_by_id(self, id: str) -> Client | None:
        data = await (await self.session.get(url=f"{self.uri_get}/{id}")).json()
        if data['success']:
            return Client(**data['obj'][0])

    def get_vpn_urn(self, data: dict):
        data = data['settings']['clients'][0]
        return f"""vless://{data['id']}@{self.ip}:443?type=tcp&security=reality&pbk={self.pbk}=
        chrome&sni=google.com&sid=ce352f&spx=%2F&flow=xtls-rprx-vision#VLESS%20%D1%81%20{data['email']}"""