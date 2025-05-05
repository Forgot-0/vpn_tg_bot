from dataclasses import dataclass

from aiohttp import ClientSession

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseApiClient
from infrastructure.builders_params.factory import ProtocolBuilderFactory


@dataclass
class A3xUiApiClient(BaseApiClient):
    builder_factory: ProtocolBuilderFactory

    def _base_url(self, server: Server) -> str:
        cfg = server.api_config
        return f"http://{server.ip}:{cfg['panel_port']}/{cfg['panel_path']}"

    def login_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/login"

    def create_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/panel/api/inbounds/addClient"

    async def create_subscription(self, user: User, subscription: Subscription, server: Server) -> None:
        async with ClientSession() as session:
            cookie = (await session.post(self.login_url(server=server))).cookies

            for config in server.protocol_configs:
                if config.protocol_type in subscription.protocol_types:
                    builder = self.builder_factory.get(server.api_type, config)
                    resp = await session.post(
                        url=self.create_url(server=server),
                        json=builder.build_params(user=user, subscription=subscription, server=server),
                        cookies=cookie
                    )

                    resp = await resp.json()

                    if not resp['success']:
                        pass 

    async def upgrade_client(self, user: User, subscription: Subscription, server: Server) -> None:
        ...

    async def delete_inactive_clients(self) -> None: ...