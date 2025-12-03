from collections import defaultdict
from app.domain.values.servers import VPNConfig
from app.infrastructure.tgbot.base import BaseTelegramBot


class MockTelegramBot(BaseTelegramBot):
    def __init__(self):
        self.data: dict[int, list[str]] = defaultdict(list)

    async def send_message(self, telegram_id: int, text: str, parse_mode: str):
        self.data[telegram_id].append(text)
    
    async def send_vpn_configs(self, telegram_id: int, vpn_configs: list[VPNConfig]):
        for cfg in vpn_configs:
            self.data[telegram_id].append(cfg.config)