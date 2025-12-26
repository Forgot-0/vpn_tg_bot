from uuid import UUID
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka

from app.application.commands.payment.paid import PaidPaymentCommand
from app.application.commands.subscriptions.create import CreateSubscriptionCommand
from app.application.commands.subscriptions.renew import RenewSubscriptionCommand
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.queries.subscription.get_by_id import GetByIdQuery
from app.application.queries.subscription.get_by_user import GetSubscriptionsUserQuery
from app.application.queries.subscription.get_config import GetConfigQuery
from app.bot.deps import user_jwt_getter
from app.bot.messages.config import ConfigMessage
from app.bot.messages.menu import VPNButton
from app.bot.messages.subscription import (
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
from app.bot.states.subscription import RenewSubscriptionStates, CreateSubscriptionStates
from app.infrastructure.mediator.base import BaseMediator


router = Router()


@router.callback_query(F.data==VPNButton.callback_data)
async def subscriptions(
    callback_query: types.CallbackQuery,
    mediator: FromDishka[BaseMediator],
) -> None:
    jwt_data = await user_jwt_getter(mediator, callback_query)
    subscriptions: list[SubscriptionDTO] = await mediator.handle_query(
        GetSubscriptionsUserQuery(
            user_jwt_data=jwt_data,
            user_id=UUID(jwt_data.id)
        )
    )
    await callback_query.message.edit_media(**ListSubscriptionMessage().build(subscriptions))
    await callback_query.answer()

@router.callback_query(F.data==AddSubscriptionButtton.callback_data)
async def add_subs(callback_query: types.CallbackQuery, state: FSMContext) -> None:
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
    ) -> None:
    await state.update_data(devices=callback_data.device)
    await callback_query.message.edit_media(**ProtocolTypeMessage().build())
    await state.set_state(CreateSubscriptionStates.waiting_for_protocol)
    await callback_query.answer()

@router.callback_query(ProtocolTypeCallbackData.filter(), CreateSubscriptionStates.waiting_for_protocol)
async def process_protocol(
        callback_query: types.CallbackQuery,
        callback_data: ProtocolTypeCallbackData,
        state: FSMContext,
        mediator: FromDishka[BaseMediator],
    ) -> None:

    data = await state.get_data()
    days = data.get("days", 30)
    devices = data.get("devices", 1)

    command = CreateSubscriptionCommand(
        duration=days,
        device_count=devices,
        protocol_types=[callback_data.protocol_type],
        user_jwt_data=await user_jwt_getter(mediator, callback_query)
    )

    payment_response, *_ = await mediator.handle_command(command)
    await callback_query.message.edit_media(**BuySubscriptionMessage().build(payment_response))

    payment_id = payment_response.url.split("=")[-1]
    await mediator.handle_command(PaidPaymentCommand(UUID(payment_id)))
    await callback_query.answer()
    await state.clear()

@router.callback_query(SubscriptionCallbackData.filter())
async def subscription(
        callback_query: types.CallbackQuery,
        callback_data: SubscriptionCallbackData,
        state: FSMContext,
        mediator: FromDishka[BaseMediator],
) -> None:
    subscription: SubscriptionDTO = await mediator.handle_query(
        GetByIdQuery(
            callback_data.subscription_id,
            user_jwt_data=await user_jwt_getter(mediator, callback_query)
        )
    )
    await state.set_state(RenewSubscriptionStates.subscription_id)
    await state.update_data(subscription_id=subscription.id.hex)

    data = SubscriptionMessage().build(subscription)
    await callback_query.message.edit_media(**data)


@router.callback_query(F.data==GetConfigSubscriptionButton.callback_data, RenewSubscriptionStates.subscription_id)
async def get_config(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        mediator: FromDishka[BaseMediator],
) -> None:
    data = await state.get_data()

    configs = await mediator.handle_query(
        GetConfigQuery(
            subscription_id=UUID(data['subscription_id']),
            user_jwt_data=await user_jwt_getter(mediator, callback_query)
        )
    )

    await callback_query.message.edit_media(**ConfigMessage().build(configs))

    await state.clear()
    await callback_query.answer()


@router.callback_query(F.data==RenewSubscriptionButton.callback_data, RenewSubscriptionStates.subscription_id)
async def renew_duration(
        callback_query: types.CallbackQuery,
        state: FSMContext) -> None:
    await callback_query.message.edit_media(**DaysMessage().build())
    await state.set_state(RenewSubscriptionStates.renew)
    await callback_query.answer()


@router.callback_query(DaysCallbackData.filter(), RenewSubscriptionStates.renew)
async def renew(
        callback_query: types.CallbackQuery,
        callback_data: DaysCallbackData,
        state: FSMContext,
        mediator: FromDishka[BaseMediator],
) -> None:
    data = await state.get_data()
    payment_response, *_ = await mediator.handle_command(
        RenewSubscriptionCommand(
            subscription_id=UUID(data['subscription_id']),
            duration=callback_data.days,
            user_jwt_data=await user_jwt_getter(mediator, callback_query)
        )
    )
    await callback_query.message.edit_media(**BuySubscriptionMessage().build(payment_response))

    payment_id = payment_response.url.split("=")[-1]
    await mediator.handle_command(PaidPaymentCommand(UUID(payment_id)))
    await state.clear()
    await callback_query.answer()

