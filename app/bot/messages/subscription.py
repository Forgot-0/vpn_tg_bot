from typing import Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from application.dtos.payments.url import PaymentDTO
from bot.messages.base import BaseMessageBuilder, BaseMediaBuilder
from bot.messages.menu import BackButton
from domain.values.servers import ProtocolType


class DaysCallbackData(CallbackData, prefix="duration"):
    days: int

class DeviceCallbackData(CallbackData, prefix="device"):
    device: int

class RegionCallbackData(CallbackData, prefix="region"):
    flag: str
    code: str
    name: str

class ProtocolTypeCallbackData(CallbackData, prefix="protocol"):
    protocol_type: str


class DaysMessage(BaseMediaBuilder):
    _photo = "AgACAgIAAxkBAAILvWgnq8qt76O702nMG3dcVBPQadjOAALp-zEb7xNBSZSYhD2OYhYXAQADAgADcwADNgQ"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎟 1 месяц 🎟", callback_data=DaysCallbackData(days=30).pack()),
                InlineKeyboardButton(text="🎫 3 месяца 🎫", callback_data=DaysCallbackData(days=60).pack()),
            ],
            [
                InlineKeyboardButton(text="🏆 6 месяцев 🏆", callback_data=DaysCallbackData(days=90).pack()),
                InlineKeyboardButton(text="💎 1 год 💎", callback_data=DaysCallbackData(days=180).pack()),
            ],
            [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
        ]
    )

class DeviceMessage(BaseMediaBuilder):
    _photo = "AgACAgIAAxkBAAILvmgnq-UPxzIOOC-tTrofE0uTI-VHAALr-zEb7xNBScYqEjkLO7CNAQADAgADcwADNgQ"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data=DeviceCallbackData(device=1).pack()),
                InlineKeyboardButton(text="2", callback_data=DeviceCallbackData(device=2).pack()),
            ],
            [
                InlineKeyboardButton(text="5", callback_data=DeviceCallbackData(device=5).pack()),
                InlineKeyboardButton(text="10", callback_data=DeviceCallbackData(device=10).pack()),
            ],
            [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
        ]
    )


class ProtocolTypeMessage(BaseMediaBuilder):
    _photo = "AgACAgIAAxkBAAILt2gnncEdg0JyRFVrCMOCat3Om1bDAAJM_jEb-kBASXPVU5fJG_HSAQADAgADcwADNgQ"
    _caption = "Выберите протокол VPN"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=protocol_type.value,
                callback_data=ProtocolTypeCallbackData(protocol_type=protocol_type.value).pack()
            )] 
            for protocol_type in ProtocolType
        ][:-1] + [[InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]]
    )


class SubscriptionMessage(BaseMediaBuilder):
    _photo = "AgACAgIAAxkBAAILtmgnnU-QDz8MRUWY4gwBTOeO5G6sAAJK_jEb-kBAST_2GxHYWDLYAQADAgADcwADNgQ"
    _caption = ""
    _reply_markup = None


    def build(self, payment_data: PaymentDTO) -> dict[str, Any]:
        content = super().build()
        content['media'].caption = f"Стоимость подписки {payment_data.price}"
        content["reply_markup"] = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Оплатить", url=payment_data.url)],
                [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
            ]
        )

        return content