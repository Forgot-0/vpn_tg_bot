from datetime import timedelta
from typing import Any
from uuid import UUID
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.application.dtos.payments.url import PaymentData
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.bot.messages.base import BaseMediaBuilder
from app.bot.messages.menu import BackButton, VPNButton
from app.domain.services.utils import now_utc, replace



class SubscriptionCallbackData(CallbackData, prefix="subs"):
    subscription_id: UUID

class AddSubscriptionButtton:
    text = "+ Добавить подписку"
    callback_data = "add_subscription"

class ListSubscriptionMessage(BaseMediaBuilder):
    _photo = 'menu'
    _caption = "Это список ваших подписок"
    _reply_markup = None

    def build(self, subscriptions: list[SubscriptionDTO]) -> dict[str, Any]:
        content =  super().build()
        content["reply_markup"] = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=(
                    f"Осталось: "
                    f"{max(
                        ((replace(subscription.start_date + timedelta(days=subscription.duration)))-now_utc()).days,
                        0
                    )}, "
                    f"регион: {subscription.flag}"
                    ),
                    callback_data=SubscriptionCallbackData(subscription_id=subscription.id).pack()
                )]
                for subscription in subscriptions
            ]
        )
        content["reply_markup"].inline_keyboard.append(
            [InlineKeyboardButton(
                text=AddSubscriptionButtton.text,
                callback_data=AddSubscriptionButtton.callback_data
                )
            ]
        )
        content['reply_markup'].inline_keyboard.append(
            [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
        )
        return content

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
    _photo = ('duration')
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎟 1 месяц 🎟", callback_data=DaysCallbackData(days=30).pack()),
                InlineKeyboardButton(text="🎫 3 месяца 🎫", callback_data=DaysCallbackData(days=90).pack()),
            ],
            [
                InlineKeyboardButton(text="🏆 6 месяцев 🏆", callback_data=DaysCallbackData(days=180).pack()),
                InlineKeyboardButton(text="💎 1 год 💎", callback_data=DaysCallbackData(days=360).pack()),
            ],
            [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
        ]
    )

class DeviceMessage(BaseMediaBuilder):
    _photo = ('device_count')
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
    _photo = ('type_vpn')
    _caption = "Выберите протокол VPN"
    _reply_markup = None

    def build(self, protocols: list[str]) -> dict[str, Any]:
        self._reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=protocol_type,
                        callback_data=ProtocolTypeCallbackData(protocol_type=protocol_type).pack()
                    )] 
                    for protocol_type in protocols
                ] + [[InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]]
            )
        
        return super().build()

class BuySubscriptionMessage(BaseMediaBuilder):
    _photo = ('buy')
    _caption = ""
    _reply_markup = None

    def build(self, payment_data: PaymentData) -> dict[str, Any]:
        content = super().build()
        content['media'].caption = f"Стоимость подписки {payment_data.price}"
        content["reply_markup"] = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Оплатить", url=payment_data.url)],
                [InlineKeyboardButton(text=BackButton.text, callback_data=BackButton.callback_data)]
            ]
        )

        return content

class RenewSubscriptionButton:
    text = "Продлить ⏱️"
    callback_data = "renew"

class GetConfigSubscriptionButton:
    text = "Получить 🔐"
    callback_data = "get_config"

class ChangeRegionSubscriptionButton:
    text = "Изменить"
    callback_data = "change_region"

class SubscriptionMessage(BaseMediaBuilder):
    _photo = ('menu')
    _caption = ""
    _reply_markup = None

    def build(self, subscription: SubscriptionDTO) -> dict[str, Any]:
        content =  super().build()
        left = replace(subscription.start_date + timedelta(days=subscription.duration))-now_utc()
        if left.days < 0: left = 0
        content['media'].caption = (
            f"Ваша подписка\n"
            f"Осталось: {left}\n"
            f"Регион: {subscription.flag}\n"
            f"Кол-во устройств: {subscription.device_count}"
        )
        content['reply_markup'] = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=GetConfigSubscriptionButton.text,
                        callback_data=GetConfigSubscriptionButton.callback_data
                    ),
                    InlineKeyboardButton(
                        text=RenewSubscriptionButton.text,
                        callback_data=RenewSubscriptionButton.callback_data
                    ),
                    InlineKeyboardButton(
                        text=f"{ChangeRegionSubscriptionButton.text} {subscription.flag}",
                        callback_data=ChangeRegionSubscriptionButton.callback_data
                    )
                ],
                [InlineKeyboardButton(text=VPNButton.text, callback_data=VPNButton.callback_data)]
            ]
        )

        return content
