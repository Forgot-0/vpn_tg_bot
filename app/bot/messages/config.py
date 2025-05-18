from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.messages.base import BaseMediaBuilder
from bot.messages.menu import BackButton
from domain.values.servers import ProtocolType, VPNConfig



def vless_reply_markup_config_builder() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            []
        ]
    )


def get_reply_markup_config_builder(protocol_type: ProtocolType) -> InlineKeyboardMarkup:
    match protocol_type:
        case ProtocolType.vless:
            return vless_reply_markup_config_builder()
    raise


class ConfigMessage(BaseMediaBuilder):
    _photo = "AgACAgIAAxkBAAILuWgnngoR_nxX7vX1R5NVJCrPltJsAAJO_jEb-kBASZj30nWKgZFtAQADAgADcwADNgQ"
    _caption = (
        "Вот ваш ключ для подключения \n"
    )
    _reply_markup = None

    def build(self, config: VPNConfig) -> dict[str, Any]:
        content = super().build()
        content['media'].caption += f"```{config.config}```"

        content['media'].parse_mode = "MarkdownV2"
        content['reply_markup'] = get_reply_markup_config_builder(config.protocol_type)
        content['reply_markup'].inline_keyboard.append(
            [
                InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)
            ]
        )
        return content