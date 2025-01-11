from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message

from application.commands.users.create import CreateUserCommand
from application.mediator.mediator import Mediator
from bot.messages.menu import BackMainMenu
from bot.messages.start import StartMessageBuilder


router = Router()


@router.message(Command("start"))
async def start(message: Message, mediator: Mediator):

    referred_by = message.text.split()
    if len(referred_by) == 2:
        referred_by = int(referred_by[1])
    else:
        referred_by = None

    await mediator.handle_command(CreateUserCommand(
        id=message.from_user.id,
        is_premium=message.from_user.is_premium,
        username=message.from_user.username,
        fullname=f"{message.from_user.first_name}-{message.from_user.last_name}",
        phone=None,
        referred_by=referred_by
    ))

    data = StartMessageBuilder().build()
    await message.answer(**data)

@router.message(F.text==BackMainMenu.BACK)
async def start(message: Message):
    data = StartMessageBuilder().build()
    await message.answer(text="Используйте меню: ", reply_markup=data['reply_markup'])