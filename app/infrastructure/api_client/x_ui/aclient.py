from dataclasses import dataclass
from http.cookies import SimpleCookie

from aiohttp import ClientSession

from app.domain.entities.server import Server
from app.domain.entities.subscription import Subscription
from app.domain.entities.user import User
from app.domain.services.ports import BaseApiClient
from app.domain.services.servers import SecureService
from app.domain.values.servers import ProtocolConfig, ProtocolType, SubscriptionConfig, VPNConfig
from app.infrastructure.builders_params.factory import ProtocolBuilderFactory
from app.application.exception import ApiClientException


@dataclass
class A3xUiApiClient(BaseApiClient):
    builder_factory: ProtocolBuilderFactory
    secure_service: SecureService

    def _base_url(self, server: Server) -> str:
        cfg = server.api_config
        protocol_http = "https" if cfg.domain else "http"
        return f"{protocol_http}://{cfg.domain}:{cfg.panel_port}/{cfg.panel_path}"

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

    def panel_settings(self, server: Server) -> str:
        return f"{self._base_url(server)}/panel/setting/defaultSettings"

    async def _login(self, session: ClientSession, server: Server) -> SimpleCookie:
        auth_credits = {
            "username": self.secure_service.decrypt(server.auth_credits.username),
            "password": self.secure_service.decrypt(server.auth_credits.password),
            "twoFactorCode": (
                self.secure_service.decrypt(server.auth_credits.twoFactorCode)
                if server.auth_credits.twoFactorCode else None
            ),
        }
        resp_login = await session.post(
            self.login_url(server=server),
            data=auth_credits
        )
        return resp_login.cookies

    async def get_protocols(self, server: Server)  -> list[ProtocolConfig]:
        protocol_configs: list[ProtocolConfig] = []

        async with ClientSession() as session:
            auth_cookies = await self._login(session=session, server=server)
            resp = await session.get(
                url=self.get_config_url(server=server),
                cookies=auth_cookies,
            )

            inbounds = await resp.json()
            if not inbounds['success']:
                raise ApiClientException(detail=inbounds)

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

    async def get_subscription_info(self, server: Server) -> SubscriptionConfig | None:
        async with ClientSession() as session:
            auth_cookies = await self._login(session=session, server=server)
            resp = await session.post(
                url=self.panel_settings(server),
                cookies=auth_cookies
            )
            all_config = await resp.json()
            all_config = all_config['obj']
            if all_config['subEnable'] == True:
                if server.api_config.domain is None:
                    raise

                cfg = SubscriptionConfig.from_url(
                    all_config['subURI']
                )

                return cfg

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
                            url=self.upgrade_url(server=server, id=str(subscription.id.value)),
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
                            id=str(subscription.id.value)
                        ),
                        json=json,
                        cookies=auth_cookies
                    )

                    resp = await resp.json()

    async def get_configs_vpn(self, user: User, subscription: Subscription, server: Server) -> list[VPNConfig]:
        configs = []
        if server.subscription_config is not None:
            configs.append(
                VPNConfig(
                    protocol_type=None,
                    config=server.subscription_config.url+subscription.id.as_generic_type()
                )
            )
        else:
            for protocol in subscription.protocol_types:
                builder = self.builder_factory.get(server.api_type, protocol)
                configs.append(builder.builde_config_vpn(user, subscription, server))

        return configs
