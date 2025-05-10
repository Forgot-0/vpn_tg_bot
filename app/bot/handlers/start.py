from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from application.commands.users.create import CreateUserCommand
from application.mediator.mediator import Mediator
from bot.messages.start import StartMessageBuilder


router = Router()


@router.message(Command("start"))
async def start(message: Message, mediator: Mediator):

    referred_by = message.text.split() # type: ignore
    if len(referred_by) == 2:
        referred_by = (referred_by[1])
    else:
        referred_by = None

    if not message.from_user: raise

    await mediator.handle_command(CreateUserCommand(
        tg_id=message.from_user.id,
        is_premium=message.from_user.is_premium,
        username=message.from_user.username,
        fullname=f"{message.from_user.first_name}-{message.from_user.last_name}",
        phone=None,
        referred_by=referred_by
    ))

    data = StartMessageBuilder().build()
    await message.answer(**data) # type: ignore