from abc import ABC
from dataclasses import dataclass

from domain.values.servers import VPNConfig



@dataclass
class BaseTelegramBot(ABC):
    async def send_message(self, telegram_id: int, text: str, parse_mode: str): ...

    async def send_vpn_configs(self, telegram_id: int, vpn_configs: list[VPNConfig]): ...