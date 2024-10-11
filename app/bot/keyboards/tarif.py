from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




class TarifsTextButtons:
    ONE_MONTH = 'ONE_MONTH'
    THREE_MONTH = 'THREE_MONTH'
    SIX_MONTH = 'SIX_MONTH'
    ONE_YEAR = 'ONE_YEAR'
    BACK = 'BACK'


def keyboard_tarifs() -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text=TarifsTextButtons.ONE_YEAR), KeyboardButton(text=TarifsTextButtons.SIX_MONTH)],
        [KeyboardButton(text=TarifsTextButtons.THREE_MONTH), KeyboardButton(text=TarifsTextButtons.ONE_MONTH)],
        [KeyboardButton(text=TarifsTextButtons.BACK)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list, 
        resize_keyboard=True, 
        input_field_placeholder='Воспользуйтесь меню:'
    )
    return keyboard