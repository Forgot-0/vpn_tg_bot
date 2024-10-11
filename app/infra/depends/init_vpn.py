

from aiohttp import ClientSession
from infra.vpn_service.aivpn_service import AIVpnService
from settings.config import Config


def init_vpn_service(config: Config) -> AIVpnService:
    return AIVpnService(
        ip=config.vpn.ip,
        main_url=config.vpn.url,
        pbk=config.vpn.pbk,
        username=config.vpn.username,
        password=config.vpn.password,
        secret=config.vpn.secret,
        urn_login=config.vpn.urn_login,
        urn_get=config.vpn.urn_get,
        urn_delete=config.vpn.urn_delete,
        urn_create=config.vpn.urn_create,
        urn_update=config.vpn.urn_update,
        session=ClientSession()
    )