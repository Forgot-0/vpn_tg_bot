
from aiogram import F, Router
from aiogram.types import Message

from application.mediator.mediator import Mediator
from application.queries.subscriptions.get import GetListSubscriptionQuery
from bot.messages.menu import HelpMessage, MenuTextButtons
from bot.messages.tarifs import TarifsMessage


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


@router.message(F.text==MenuTextButtons.HELP)
async def help(message: Message):
    await message.delete()
    data = HelpMessage().build()
    await message.answer(**data)