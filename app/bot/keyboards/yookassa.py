from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData




class CheckPayCallbackData(CallbackData, prefix='check'):
    payment_id: str


def yoo_kassa_keyboard(payment_url: str, payment_id: str):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text='Оплатить', url=payment_url),
    )

    return builder.as_markup()