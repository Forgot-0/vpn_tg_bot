from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.messages.base import BaseMessageBuilder, BaseMediaBuilder


class VPNButton:
    text = "🔐 VPN"
    callback_data = "vpn"

class HelpButton:
    text = "🆘 Поддержка"
    url = "https://t.me/VPNHE1P"
    callback_data = "help"

class RewardButton:
    text = "🎁 Реферальная система"
    callback_data = "reward"

class AboutButton:
    text = "📄 О нас"
    callback_data = "about"

class BackButton:
    text = "🔙 Главное меню"
    callback_data = "back"


def get_menu_keyboards() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=VPNButton.text, callback_data=VPNButton.callback_data)],
            [InlineKeyboardButton(text=HelpButton.text, callback_data=HelpButton.callback_data)],
            [InlineKeyboardButton(text=RewardButton.text, callback_data=RewardButton.callback_data)],
            [InlineKeyboardButton(text=AboutButton.text, callback_data=AboutButton.callback_data)]
        ]
    )
    return keyboard


class StartMessageBuilder(BaseMediaBuilder):
    _photo = 'menu'
    _reply_markup = get_menu_keyboards()
    


class HelpMessage(BaseMediaBuilder):
    _photo = 'help'
    _caption = "Напишите свою проблему сюда 👇"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=HelpButton.text, url=HelpButton.url)],
            [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
        ]
    )

class AboutMessage(BaseMediaBuilder):
    _photo = 'about'
    _caption = (
        ""
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
        ]
    )

