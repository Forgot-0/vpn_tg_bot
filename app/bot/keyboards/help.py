from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

class HelpTextButton:
    user: str = 'https://t.me/VPNHE1P'
    text: str = '🆘 Помощь 🆘'


def help_keayboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text=HelpTextButton.text, url=HelpTextButton.user),
    )
    return builder.as_markup()