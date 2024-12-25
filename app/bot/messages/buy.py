from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from application.dto.subscription import SubscriptionDTO


class BuyMessage:
    _text: str = "Выбирите тариф👇"
    _reply_markup = ...

    def build(self, subscriptions: list[SubscriptionDTO]):
        inline_keyboard = []

        for subscription in subscriptions:
            inline_keyboard.append(
                [InlineKeyboardButton(
                    text=subscription.name,
                    callback_data=f"buy_subscription/{subscription.id}"
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