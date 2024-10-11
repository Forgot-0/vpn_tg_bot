from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message

from application.commands.users.create import CreateUserCommand
from application.mediator.mediator import Mediator
from bot.keyboards.menu import keyboard_menu



router = Router()


@router.message(F.text, Command("start"))
async def start(message: Message, mediator: Mediator):
    assert message.from_user.is_bot == False
    await mediator.handle_command(CreateUserCommand(
        tg_id=message.from_user.id,
        tg_username=message.from_user.username,
        is_premium=message.from_user.is_premium
    ))
    text = """Описание бота с его коммандами


    """
    await message.answer(text, reply_markup=keyboard_menu())

