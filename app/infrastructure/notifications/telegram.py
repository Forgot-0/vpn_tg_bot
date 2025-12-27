from dataclasses import dataclass

from aiogram import Bot

from app.application.services.notifications import NotificationSevice
from app.domain.entities.user import User
from app.domain.values.servers import VPNConfig


@dataclass
class TelegramNotificationSevice(NotificationSevice):
    bot: Bot

    async def send_subscription_config(self, user: User, vpn_config: VPNConfig) -> None:
        if user.telegram_id is None:
            return

        await self.bot.send_message(
            chat_id=user.telegram_id,
            text=vpn_config.config
        )
