from enum import Enum
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.menu import BackMainMenu




class TarifsTextButtons(Enum):
    ONE_MONTH = '🎟 На 30 дней за 100 руб 🎟'
    THREE_MONTH = '🎫 На 90 дней за 300 руб 🎫'
    SIX_MONTH = '🏆 На 180 дней за 600 руб 🏆'
    ONE_YEAR = '💎 На 365 дней за 1200 руб 💎'




def keyboard_tarifs() -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text=TarifsTextButtons.ONE_YEAR), KeyboardButton(text=TarifsTextButtons.SIX_MONTH)],
        [KeyboardButton(text=TarifsTextButtons.THREE_MONTH), KeyboardButton(text=TarifsTextButtons.ONE_MONTH)],
        [KeyboardButton(text=BackMainMenu.BACK)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True, 
        input_field_placeholder='Воспользуйтесь меню:'
    )
    return keyboard