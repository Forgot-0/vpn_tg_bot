from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.services.notifications import NotificationSevice
from app.domain.entities.user import User
from app.domain.values.servers import VPNConfig


@dataclass
class TelegramNotificationSevice(NotificationSevice):
    def __init__(self, bot_token: str) -> None:
        self.bot = Bot(bot_token)

    async def send_subscription_config(self, user: User, subscription: SubscriptionDTO) -> None:
        if user.telegram_id is None:
            return

        await self.bot.send_message(
            chat_id=user.telegram_id,
            text=(
                f"🎉 <b>Подписка активирована!</b>\n\n"
                f"📅 <b>Действует до:</b> {subscription.expires_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                f"✅ Теперь вам доступны все возможности тарифа.\n"
                f"Приятного использования! 🚀"
            ),
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Получить 🔐", callback_data="get_config"),
                        InlineKeyboardButton(text="Продлить ⏱️", callback_data="renew"),
                    ],
                    [
                        InlineKeyboardButton(text="🔐 VPN", callback_data="vpn"),
                    ],
                ]
            )
        )

