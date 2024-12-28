from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.messages.base import BaseMessageBuilder


class MenuTextButtons:
    TARIFS = '💰 Тарифы'
    HELP = '🆘 Помощь'
    GUIDE = '📄 Руководство по использованию'
    REWARD = "🎁 Подарки"
    PROFILE = "👤 Профиль"


class BackMainMenu:
    BACK = '🔙 Назад'


def get_menu_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=MenuTextButtons.TARIFS), KeyboardButton(text=MenuTextButtons.PROFILE)],
                [KeyboardButton(text=MenuTextButtons.REWARD), KeyboardButton(text=MenuTextButtons.HELP)],
                [KeyboardButton(text=MenuTextButtons.GUIDE)]
            ]
        )

class HelpTextButton:
    user: str = 'https://t.me/VPNHE1P'
    text: str = '🆘 Помощь 🆘'


class HelpMessage(BaseMessageBuilder):
    _text = "Напишите свою проблему сюда 👇"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=HelpTextButton.text, url=HelpTextButton.user)]
        ]
    )