from uuid import UUID
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from application.commands.orders.create import CreateOrderCommand
from application.dto.profile import ProfileDTO
from application.mediator.mediator import Mediator
from application.queries.order.get_by_user import GetByUserOrdersQuery
from bot.messages.buy import UrlPaymentMessage
from bot.messages.menu import MenuTextButtons
from bot.messages.profile import ProfileMessage


router = Router()


@router.callback_query(F.data.contains("buy_subscription/"))
async def create_order(callback_query: CallbackQuery, mediator: Mediator):
    url, *_ = await mediator.handle_command(
        CreateOrderCommand(
            subscription_id=UUID(hex=callback_query.data.split("/")[-1]),
            user_id=callback_query.from_user.id
        )
    )
    data = UrlPaymentMessage().build(url=url)

    await callback_query.message.answer(**data)


@router.message(F.text==MenuTextButtons.PROFILE)
async def get_profile(message: Message, mediator: Mediator):
    await message.delete()
    profiles: list[ProfileDTO] = await mediator.handle_query(
        GetByUserOrdersQuery(
            user_id=message.from_user.id
        )
    )
    data = ProfileMessage().build(profiles=profiles)
    await message.answer(**data)

