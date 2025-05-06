from dataclasses import dataclass

from aiogram import Bot

from domain.values.servers import VPNConfig
from infrastructure.tgbot.base import BaseTelegramBot


@dataclass
class AiohramTelegramBot(BaseTelegramBot):
    bot: Bot

    async def send_message(self, telegram_id: int, text: str, parse_mode: str):
        await self.bot.send_message(chat_id=telegram_id, text=text, parse_mode=parse_mode)
    
    async def send_vpn_configs(self, telegram_id: int, vpn_configs: list[VPNConfig]):
        for vpn_config in vpn_configs:
            await self.bot.send_message(telegram_id, text=f"`{vpn_config.config}`", parse_mode="MarkdownV2")