from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



class MenuTextButtons:
    BUY = 'Купить'
    TARIFS = 'Тарифы'
    HELP = 'Помощь'


def keyboard_menu() -> ReplyKeyboardMarkup:

    kb_list = [
        [KeyboardButton(text=MenuTextButtons.BUY)],
        [KeyboardButton(text=MenuTextButtons.TARIFS), KeyboardButton(text=MenuTextButtons.HELP)]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list, 
        resize_keyboard=True, 
        input_field_placeholder='Воспользуйтесь меню:'
    )
    return keyboard