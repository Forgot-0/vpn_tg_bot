from uuid import UUID
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from application.commands.subscriptions.create import CreateSubscriptionCommand
from application.commands.subscriptions.renew import RenewSubscriptionCommand
from application.dtos.subsciprions.subscription import SubscriptionDTO
from application.queries.subscription.get_by_id import GetByIdQuery
from application.queries.subscription.get_by_tgid import GetByTgIdQuery
from application.queries.subscription.get_config import GetConfigQuery
from bot.messages.config import ConfigMessage
from bot.messages.menu import VPNButton
from bot.messages.subscription import (
    AddSubscriptionButtton,
    DaysCallbackData,
    DaysMessage,
    DeviceCallbackData,
    DeviceMessage,
    GetConfigSubscriptionButton,
    ListSubscriptionMessage,
    ProtocolTypeCallbackData,
    ProtocolTypeMessage,
    BuySubscriptionMessage,
    RenewSubscriptionButton,
    SubscriptionCallbackData,
    SubscriptionMessage
)
from bot.states.subscription import RenewSubscriptionStates, CreateSubscriptionStates
from infrastructure.mediator.mediator import Mediator


router = Router()


@router.callback_query(F.data==VPNButton.callback_data)
async def subscriptions(callback_query: types.CallbackQuery, state: FSMContext, mediator: Mediator):
    subscriptions: list[SubscriptionDTO] = await mediator.handle_query(GetByTgIdQuery(callback_query.from_user.id))
    await callback_query.message.edit_media(**ListSubscriptionMessage().build(subscriptions))
    await callback_query.answer()

@router.callback_query(F.data==AddSubscriptionButtton.callback_data)
async def add_subs(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_media(**DaysMessage().build()) # type: ignore
    await state.set_state(CreateSubscriptionStates.waiting_for_days)
    await callback_query.answer()

@router.callback_query(DaysCallbackData.filter(), CreateSubscriptionStates.waiting_for_days)
async def process_days(
        callback_query: types.CallbackQuery,
        callback_data: DaysCallbackData,
        state: FSMContext
    ):
    await state.update_data(days=callback_data.days)
    await callback_query.message.edit_media(**DeviceMessage().build())
    await state.set_state(CreateSubscriptionStates.waiting_for_devices)
    await callback_query.answer()

@router.callback_query(DeviceCallbackData.filter(), CreateSubscriptionStates.waiting_for_devices)
async def process_devices(
        callback_query: types.CallbackQuery,
        callback_data: DeviceCallbackData,
        state: FSMContext
    ):
    await state.update_data(devices=callback_data.device)
    await callback_query.message.edit_media(**ProtocolTypeMessage().build())
    await state.set_state(CreateSubscriptionStates.waiting_for_protocol)
    await callback_query.answer()

@router.callback_query(ProtocolTypeCallbackData.filter(), CreateSubscriptionStates.waiting_for_protocol)
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
    await callback_query.message.edit_media(**BuySubscriptionMessage().build(payment_response))

    await callback_query.answer()
    await state.clear()

@router.callback_query(SubscriptionCallbackData.filter())
async def subscription(
        callback_query: types.CallbackQuery,
        callback_data: SubscriptionCallbackData,
        state: FSMContext,
        mediator: Mediator):
    subscription: SubscriptionDTO = await mediator.handle_query(GetByIdQuery(callback_data.subscription_id))
    await state.set_state(RenewSubscriptionStates.subscription_id)
    await state.update_data(subscription_id=subscription.id.hex)

    data = SubscriptionMessage().build(subscription)
    await callback_query.message.edit_media(**data)

@router.callback_query(F.data==GetConfigSubscriptionButton.callback_data, RenewSubscriptionStates.subscription_id)
async def get_config(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        mediator: Mediator):
    data = await state.get_data()

    configs = await mediator.handle_query(GetConfigQuery(UUID(data['subscription_id'])))

    await callback_query.message.edit_media(**ConfigMessage().build(configs))

    await state.clear()
    await callback_query.answer()


@router.callback_query(F.data==RenewSubscriptionButton.callback_data, RenewSubscriptionStates.subscription_id)
async def renew_duration(
        callback_query: types.CallbackQuery,
        state: FSMContext):
    await callback_query.message.edit_media(**DaysMessage().build())
    await state.set_state(RenewSubscriptionStates.renew)
    await callback_query.answer()


@router.callback_query(DaysCallbackData.filter(), RenewSubscriptionStates.renew)
async def renew(
        callback_query: types.CallbackQuery,
        callback_data: DaysCallbackData,
        state: FSMContext,
        mediator: Mediator):
    data = await state.get_data()
    payment_response, *_ = await mediator.handle_command(
        RenewSubscriptionCommand(
            subscription_id=UUID(data['subscription_id']),
            duration=callback_data.days
        )
    )
    await callback_query.message.edit_media(**BuySubscriptionMessage().build(payment_response))

    payment_id = payment_response.url.split("=")[-1]
    await state.clear()
    await callback_query.answer()


