from dataclasses import dataclass
from http.cookies import SimpleCookie

from aiohttp import ClientSession

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseApiClient
from domain.services.servers import decrypt
from domain.values.servers import ProtocolConfig, ProtocolType
from infrastructure.builders_params.factory import ProtocolBuilderFactory


@dataclass
class A3xUiApiClient(BaseApiClient):
    builder_factory: ProtocolBuilderFactory

    def _base_url(self, server: Server) -> str:
        cfg = server.api_config
        return f"http://{cfg['ip']}:{cfg['panel_port']}/{cfg['panel_path']}"

    def login_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/login/"

    def create_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/panel/api/inbounds/addClient"

    def upgrade_url(self, server: Server, id: str) -> str:
        return f"{self._base_url(server)}/panel/api/inbounds/updateClient/{id}"

    def delete_client_url(self, server: Server, inbound_id: int, id: str) -> str:
        return f"{self._base_url(server)}/panel/api/inbounds/{inbound_id}/delClient/{id}"

    def get_config_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/panel/api/inbounds/list"

    async def _login(self, session: ClientSession, server: Server) -> SimpleCookie:
        for key, value in server.auth_credits.items():
                server.auth_credits[key] = decrypt(value)

        resp_login = await session.post(
            self.login_url(server=server),
            data=server.auth_credits
        )
        return resp_login.cookies

    async def get_configs(self, server: Server)  -> list[ProtocolConfig]:
        protocol_configs = []

        async with ClientSession() as session:
            auth_cookies = await self._login(session=session, server=server)
            resp = await session.get(
                url=self.get_config_url(server=server),
                cookies=auth_cookies
            )

        inbounds = await resp.json()
        if not inbounds['success']:
            raise 

        for ind in inbounds['obj']:
            protocol_type = ProtocolType(ind['protocol'])
            builder = self.builder_factory.get(server.api_type, protocol_type)
            protocol_configs.append(
                ProtocolConfig(
                    config=builder.build_config(ind),
                    protocol_type=protocol_type
                    )
            )

        return protocol_configs

    async def create_or_upgrade_subscription(
            self,
            user: User,
            subscription: Subscription,
            server: Server
        ) -> None:

        async with ClientSession() as session:
            auth_cookies = await self._login(session=session, server=server)

            for protocol_type in server.protocol_configs:
                builder = self.builder_factory.get(server.api_type, protocol_type)
                json = builder.build_params(user=user, subscription=subscription, server=server)
                if protocol_type in subscription.protocol_types:

                    resp = await session.post(
                        url=self.create_url(server=server),
                        json=json,
                        cookies=auth_cookies
                    )

                    resp = await resp.json()

                    if "Duplicate email:" in resp.get("msg", ""):
                        resp = await session.post(
                            url=self.upgrade_url(server=server, id=str(subscription.id.value.hex)),
                            json=json,
                            cookies=auth_cookies
                        )

    async def delete_inactive_clients(self) -> None: ...

    async def delete_client(
            self,
            user: User,
            subscription: Subscription,
            server: Server
        ) -> None:

        async with ClientSession() as session:
            auth_cookies = await self._login(session=session, server=server)

            for protocol_type in server.protocol_configs:
                builder = self.builder_factory.get(server.api_type, protocol_type)
                json = builder.build_params(user=user, subscription=subscription, server=server)

                if protocol_type in subscription.protocol_types:

                    resp = await session.post(
                        url=self.delete_client_url(
                            server=server,
                            inbound_id=server.protocol_configs[protocol_type].config['inbound_id'],
                            id=str(subscription.id.value.hex)
                        ),
                        json=json,
                        cookies=auth_cookies
                    )

                    resp = await resp.json()
