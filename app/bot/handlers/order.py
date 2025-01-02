from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from application.commands.orders.create import CreateOrderCommand
from application.dto.profile import ProfileDTO
from application.dto.subscription import SubscriptionDTO
from application.mediator.mediator import Mediator
from application.queries.subscriptions.get import GetListSubscriptionQuery
from application.queries.users.get_profile import GetProfileVpnQuery
from bot.messages.buy import BuyMessage, BuyOrderCallback, UrlPaymentMessage
from bot.messages.menu import MenuTextButtons
from bot.messages.profile import ProfileMessage
from bot.messages.tarifs import BuyBotton


router = Router()


@router.callback_query(BuyOrderCallback.filter())
async def create_order(callback_query: CallbackQuery, callback_data: BuyOrderCallback,  mediator: Mediator):
    await callback_query.answer()
    url, *_ = await mediator.handle_command(
        CreateOrderCommand(
            subscription_id=callback_data.subscription_id,
            user_id=callback_query.from_user.id,
        )
    )
    data = UrlPaymentMessage().build(url=url)
    await callback_query.message.delete()
    await callback_query.message.answer(**data)

@router.callback_query(F.data==BuyBotton.callback_data)
async def buy_vpn(callback_query: CallbackQuery, mediator: Mediator):
    subscriptions: list[SubscriptionDTO] = await mediator.handle_query(
        GetListSubscriptionQuery(
            user_id=callback_query.from_user.id
        )
    )

    data = BuyMessage().build(subscriptions=subscriptions)
    await callback_query.message.answer(**data)

@router.message(F.text==MenuTextButtons.PROFILE)
async def get_profile(message: Message, mediator: Mediator):
    await message.delete()
    profile: ProfileDTO = await mediator.handle_query(
        GetProfileVpnQuery(
            user_id=message.from_user.id
        )
    )
    data = ProfileMessage().build(profile=profile)
    await message.answer(**data)

