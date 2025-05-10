from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class VPNButton:
    text = "🔐 VPN"
    callback_data = "vpn"

class HelpButton:
    text = "🆘 Поддержка"
    callback_data = "support"

class RewardButton:
    text = "🎁 Реферальная система"
    callback_data = "reward"

class AboutButton:
    text = "📄 О нас"
    callback_data = "about"

class BackButton:
    text = "🔙 Назад"
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