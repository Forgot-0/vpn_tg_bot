from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message

from application.commands.users.create import CreateUserCommand
from application.mediator.mediator import Mediator
from bot.messages.start import StartMessageBuilder


router = Router()


@router.message(F.text, Command("start"))
async def start(message: Message, mediator: Mediator):
    await mediator.handle_command(CreateUserCommand(
        id=message.from_user.id,
        is_premium=message.from_user.is_premium,
        username=message.from_user.username,
        fullname=f"{message.from_user.first_name}-{message.from_user.last_name}",
        phone=None
    ))

    data = StartMessageBuilder().build()
    await message.answer(**data)