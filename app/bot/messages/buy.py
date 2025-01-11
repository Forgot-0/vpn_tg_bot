from uuid import UUID
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from application.dto.subscription import SubscriptionDTO



class BuyOrderCallback(CallbackData, prefix="buy_subscription"):
    subscription_id: UUID


class BuyMessage:
    _text: str = "Выбирите тариф👇"
    _reply_markup = ...

    def build(self, subscriptions: list[SubscriptionDTO]):
        inline_keyboard = []

        for subscription in subscriptions:
            inline_keyboard.append(
                [InlineKeyboardButton(
                    text=subscription.name,
                    callback_data=BuyOrderCallback(
                        subscription_id=subscription.id,
                    ).pack()
                )]
            )

        self._reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        content = {"text": self._text}
        content["reply_markup"] = self._reply_markup

        return content


class UrlPaymentMessage:
    _text: str = "Оплатите подписку 👇"
    _reply_markup = ...

    def build(self, url: str):
        self._reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='YooKass', url=url)]
            ]
        )

        content = {"text": self._text}
        content["reply_markup"] = self._reply_markup

        return content