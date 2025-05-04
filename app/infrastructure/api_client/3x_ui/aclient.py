from dataclasses import dataclass
from http.cookies import SimpleCookie

from aiohttp import ClientSession

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseApiClient
from infrastructure.builders_params.factory import ProtocolBuilderFactory


@dataclass
class A3xUiApiClient(BaseApiClient):
    session: ClientSession
    builder_factory: ProtocolBuilderFactory

    def login_url(self, server: Server) -> str:
        return f"http://{server.ip}" + ":{panel_port}/{panel_path}/login".format(**server.api_config)

    def create_url(self, server: Server) -> str:
        return (
            f"http://{server.ip}"
            "{self.panel_port}/{self.panel_path}/panel/api/inbounds/addClient".format(**server.api_config)
            )

    async def login(self, server: Server) -> SimpleCookie:
        resp = await self.session.post(self.login_url(server=server))
        return resp.cookies

    async def create_subscription(self, user: User, subscription: Subscription, server: Server) -> None:
        cookies = await self.login(server=server)

        for config in server.protocol_configs:
            if config.protocol_type in subscription.protocol_types:
                builder = self.builder_factory.get(server.api_type, config)
                resp = await self.session.post(
                    url=self.create_url(server=server),
                    json=builder.build_params(user=user, subscription=subscription, server=server),
                    cookies=cookies
                )

                resp = await resp.json()

                if not resp['success']:
                    pass 
