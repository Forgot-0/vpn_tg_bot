from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from domain.values.servers import ProtocolType, VPNConfig
from infrastructure.tgbot.base import BaseTelegramBot


@dataclass
class AiohramTelegramBot(BaseTelegramBot):
    bot: Bot

    async def send_message(self, telegram_id: int, text: str, parse_mode: str):
        await self.bot.send_message(chat_id=telegram_id, text=text, parse_mode=parse_mode)

    async def send_vpn_configs(self, telegram_id: int, vpn_configs: list[VPNConfig]):
        for vpn_config in vpn_configs:
            await self.bot.send_photo(
                telegram_id,
                photo="AgACAgIAAxkBAAILuWgnngoR_nxX7vX1R5NVJCrPltJsAAJO_jEb-kBASZj30nWKgZFtAQADAgADcwADNgQ",
                caption=(
                    "Ваша конфигурация \n"
                    f"```{vpn_config.config}```"
                ),
                parse_mode="MarkdownV2",
                reply_markup=self.get_reply_markup_config_builder(vpn_config.protocol_type)
            )

    def vless_reply_markup_config_builder(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="🍏 Mac OS/IOS",
                    url="https://telegra.ph/Instrukciya-po-podklyucheniyu-VPN-Vless-i-ShadowSocks-dlya-IPhone-08-25"
                )],
                [InlineKeyboardButton(
                    text="🤖 Android",
                    url="https://telegra.ph/Instrukciya-po-podklyucheniyu-VPN-Vless-dlya-Android-11-18"
                )],
                [InlineKeyboardButton(
                    text="🖥 Windows",
                    url="https://telegra.ph/Instrukciya-po-podklyucheniyu-VPN-Vless-i-ShadowSocks-dlya-PK-08-25"
                )],
            ]
        )

    def get_reply_markup_config_builder(self, protocol_type: ProtocolType) -> InlineKeyboardMarkup:
        match protocol_type:
            case ProtocolType.vless:
                return self.vless_reply_markup_config_builder()
        raise