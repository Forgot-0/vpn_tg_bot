from typing import Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from bot.messages.base import BaseMessageBuilder
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


class DaysMessage(BaseMessageBuilder):
    _text = (
        "Выберите кол-во дней подписки: "
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="30 дней", callback_data=DaysCallbackData(days=30).pack()),
                InlineKeyboardButton(text="60 дней", callback_data=DaysCallbackData(days=60).pack()),
            ],
            [
                InlineKeyboardButton(text="90 дней", callback_data=DaysCallbackData(days=90).pack()),
                InlineKeyboardButton(text="180 дней", callback_data=DaysCallbackData(days=180).pack()),
            ]
        ]
    )

class DeviceMessage(BaseMessageBuilder):
    _text = (
        "Выберите кол-во устройств: "
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data=DeviceCallbackData(device=1).pack()),
                InlineKeyboardButton(text="2", callback_data=DeviceCallbackData(device=2).pack()),
            ],
            [
                InlineKeyboardButton(text="5", callback_data=DeviceCallbackData(device=5).pack()),
                InlineKeyboardButton(text="10", callback_data=DeviceCallbackData(device=10).pack()),
            ]
        ]
    )


class ProtocolTypeMessage(BaseMessageBuilder):
    _text = (
        "Выберите протокол: "
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=protocol_type.value, callback_data=protocol_type.value)] 
            for protocol_type in ProtocolType
        ][:-1]
    )

    _parse_mode = "MarkdownV2"
