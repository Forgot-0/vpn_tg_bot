from uuid import UUID
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from application.commands.order.paid import PaidOrderCommand
from application.commands.subscriptions.create import CreateSubscriptionCommand
from application.mediator.mediator import Mediator
from bot.messages.menu import VPNButton
from bot.messages.subscription import (
    DaysCallbackData,
    DaysMessage,
    DeviceCallbackData,
    DeviceMessage,
    ProtocolTypeCallbackData,
    ProtocolTypeMessage,
    SubscriptionMessage
)
from bot.states.subscription import SubscriptionStates

router = Router()


@router.callback_query(F.data==VPNButton.callback_data)
async def subscribe_command(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(**DaysMessage().build())
    await state.set_state(SubscriptionStates.waiting_for_days)

@router.callback_query(DaysCallbackData.filter(), SubscriptionStates.waiting_for_days)
async def process_days(
        callback_query: types.CallbackQuery,
        callback_data: DaysCallbackData,
        state: FSMContext
    ):
    await state.update_data(days=callback_data.days)
    await callback_query.message.edit_text(**DeviceMessage().build())
    await state.set_state(SubscriptionStates.waiting_for_devices)

@router.callback_query(DeviceCallbackData.filter(), SubscriptionStates.waiting_for_devices)
async def process_devices(
        callback_query: types.CallbackQuery,
        callback_data: DeviceCallbackData,
        state: FSMContext
    ):
    await state.update_data(devices=callback_data.device)
    await callback_query.message.edit_text(**ProtocolTypeMessage().build())
    await state.set_state(SubscriptionStates.waiting_for_protocol)

@router.callback_query(ProtocolTypeCallbackData.filter(), SubscriptionStates.waiting_for_protocol)
async def process_protocol(
        callback_query: types.CallbackQuery,
        callback_data: ProtocolTypeCallbackData,
        state: FSMContext,
        mediator: Mediator
    ):

    data = await state.get_data()
    days = data.get("days", 30)
    devices = data.get("devices", 1)

    command = CreateSubscriptionCommand(
        telegram_id=callback_query.from_user.id,
        duration=days,
        device_count=devices,
        protocol_types=[callback_data.protocol_type]
    )

    payment_response, *_ = await mediator.handle_command(command)
    await callback_query.message.edit_text(**SubscriptionMessage().build(payment_response))

    payment_id = payment_response.url.split("=")[-1]
    await mediator.handle_command(PaidOrderCommand(payment_id=UUID(hex=payment_id)))
    await state.clear()
    await callback_query.answer()