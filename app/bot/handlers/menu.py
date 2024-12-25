
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from application.dto.subscription import SubscriptionDTO
from application.mediator.mediator import Mediator
from application.queries.subscriptions.get import GetListSubscriptionQuery
from bot.messages.buy import BuyMessage
from bot.messages.menu import BackMainMenu, HelpMessage, MenuTextButtons, get_menu_keyboards
from bot.messages.tarifs import BuyBotton, TarifsMessage


router = Router()


@router.message(F.text==MenuTextButtons.TARIFS)
async def get_list_tarifs(message: Message, mediator: Mediator):
    await message.delete()
    subscriptions = await mediator.handle_query(
        GetListSubscriptionQuery(
            user_id=message.from_user.id
        )
    )
    data = TarifsMessage().build(subscriptions=subscriptions)
    await message.answer(**data)


@router.callback_query(F.data==BuyBotton.callback_data)
async def buy_vpn(callback_query: CallbackQuery, mediator: Mediator):
    subscriptions: list[SubscriptionDTO] = await mediator.handle_query(
        GetListSubscriptionQuery(
            user_id=callback_query.from_user.id
        )
    )

    data = BuyMessage().build(subscriptions=subscriptions)
    await callback_query.message.answer(**data)


@router.message(F.text==MenuTextButtons.HELP)
async def help(message: Message):
    await message.delete()
    data = HelpMessage().build()
    await message.answer(**data)