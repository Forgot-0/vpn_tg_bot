

from aiohttp import ClientSession
from infra.vpn_service.aivpn_service import AIVpnService
from settings.config import Config


def init_vpn_service(config: Config) -> AIVpnService:
    return AIVpnService(
        username=config.vpn.username,
        password=config.vpn.password,
        secret=config.vpn.secret,
        session=ClientSession()
    )