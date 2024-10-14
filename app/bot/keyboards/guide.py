from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.keyboards.menu import BackMainMenu





class TypeSystemButtons:
    IOS = "Mac OS/IOS"
    WINDOWS = "Windows"
    NEKORAY = 'Nekoray'
    LINUX = "Linux"



def type_system() -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text=TypeSystemButtons.IOS), KeyboardButton(text=TypeSystemButtons.WINDOWS)],
        [KeyboardButton(text=TypeSystemButtons.NEKORAY), KeyboardButton(text=TypeSystemButtons.LINUX)],
        [KeyboardButton(text=BackMainMenu.BACK)]
    ]
    kb = ReplyKeyboardMarkup(
        keyboard=kb_list
    )
    return kb