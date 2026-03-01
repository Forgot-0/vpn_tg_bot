from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.messages.base import BaseMediaBuilder
from app.bot.messages.menu import BackButton
from app.domain.values.servers import VPNConfig



def reply_markup_config_builder() -> InlineKeyboardMarkup:
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


class ConfigMessage(BaseMediaBuilder):
    _photo = ('menu')
    _caption = (
        "Вот ваш ключ для подключения \n"
    )
    _reply_markup = None

    def build(self, configs: list[VPNConfig]) -> dict[str, Any]:
        content = super().build()
        for cfg in configs:
            content['media'].caption += f"```{cfg.config}```"
            content['media'].parse_mode = "MarkdownV2"

        content['reply_markup'] = reply_markup_config_builder()
        content['reply_markup'].inline_keyboard.append(
            [
                InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)
            ]
        )
        return content
