from datetime import timedelta
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from application.commands.subscription.create import CreateSubscriptionCommnad
from application.mediator.mediator import Mediator
from bot.states.subscriptions import SubscriptionState
from settings.config import settings



router = Router()


@router.message(
    F.text=='/create_subscription',
    F.from_user.id==settings.bot.owner
)
async def create_subscription(message: Message, state: FSMContext):
    await message.answer("Введите имя подписки: ")
    await state.set_state(SubscriptionState.name)


@router.message(
    F.text,
    SubscriptionState.name
)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание подписки")
    await state.set_state(SubscriptionState.description)

@router.message(
    F.text,
    SubscriptionState.description
)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите длительность подписки в днях")
    await state.set_state(SubscriptionState.duration)

@router.message(
    F.text,
    SubscriptionState.duration
)
async def set_duration(message: Message, state: FSMContext):
    await state.update_data(duration=int(message.text))
    await message.answer("Введите цену подписки в формате 99.99")
    await state.set_state(SubscriptionState.price)

@router.message(
    F.text,
    SubscriptionState.price
)
async def set_price(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer("Введите лимит устройств или укажите 0")
    await state.set_state(SubscriptionState.limit_ip)

@router.message(
    F.text,
    SubscriptionState.limit_ip
)
async def set_limit_ip(message: Message, state: FSMContext):
    await state.update_data(limit_ip=int(message.text))
    await message.answer("Введите лимит трафика или укажите 0")
    await state.set_state(SubscriptionState.limit_trafic)


@router.message(
    F.text,
    SubscriptionState.limit_trafic
)
async def set_limit_trafic(message: Message, state: FSMContext, mediator: Mediator):
    await state.update_data(limit_trafic=int(message.text))
    data = await state.get_data()

    await mediator.handle_command(
        CreateSubscriptionCommnad(
            name=data['name'],
            description=data['description'],
            duration=timedelta(days=data['duration']),
            price=data['price'],
            limit_ip=data['limit_ip'],
            limit_trafic=data['limit_trafic']
        )
    )

    await message.answer("Подписка успешно созданна!")
    await state.clear()

