from dataclasses import dataclass

from aiohttp import ClientSession

from configs.app import settings
from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.ports import BaseApiClient
from domain.values.servers import VPNConfig
from infrastructure.builders_params.factory import ProtocolBuilderFactory


@dataclass
class A3xUiApiClient(BaseApiClient):
    builder_factory: ProtocolBuilderFactory

    def _base_url(self, server: Server) -> str:
        cfg = server.api_config
        return f"http://{server.ip}:{cfg['panel_port']}/{cfg['panel_path']}"

    def login_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/login/"

    def create_url(self, server: Server) -> str:
        return f"{self._base_url(server)}/panel/api/inbounds/addClient"

    async def create_subscription(self, user: User, subscription: Subscription, server: Server) -> list[VPNConfig]:
        vpn_config = []
        
        async with ClientSession() as session:
            resp_login = await session.post(
                self.login_url(server=server),
                data={
                    "username": settings.VPN_USERNAME,
                    "password": settings.VPN_PASSWORD,
                    "loginSecret": settings.VPN_SECRET
                }
            )
            for protocol_type in server.protocol_configs:
                if protocol_type in subscription.protocol_types:
                    builder = self.builder_factory.get(server.api_type, protocol_type)
                    resp = await session.post(
                        url=self.create_url(server=server),
                        json=builder.build_params(user=user, subscription=subscription, server=server),
                        cookies=resp_login.cookies
                    )
                    vpn_config.append(builder.builde_config_vpn(user=user, subscription=subscription, server=server))
                    resp = await resp.json()

                    if not resp['success']:
                        pass 

        return vpn_config

    async def upgrade_client(self, user: User, subscription: Subscription, server: Server) -> None:
        ...

    async def delete_inactive_clients(self) -> None: ...