
from dataclasses import dataclass

from httpx import AsyncClient

from app.application.interfaces.servers import PanelClient
from app.domain.entities.server import VPNServer
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import PanelType
from app.domain.values.subscriptions import AccessCredential


@dataclass
class ThreeXUIClient(PanelClient):

    client: AsyncClient

    @property
    def panel_type(self) -> PanelType:
        return PanelType.X3UI


    def login_url(self) -> str:
        return ""

    async def login(self, server: VPNServer) -> None:
        if server.panel_credentials.username is not None:
            resp = await self.client.post(
            self.login_url(), data={
                "username": server.panel_credentials.username,
                "password": server.panel_credentials.password,
                },
            )

            resp.raise_for_status()

        if server.panel_credentials.api_token is not None:
            self.client.cookies.set("Authorization", f"Bearer {server.panel_credentials.api_token}")


    async def create(self, server: VPNServer, subscription: Subscription) -> list[AccessCredential]:
        await self.login(server=server)

