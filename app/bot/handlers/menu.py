from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message

from application.commands.users.create import CreateUserCommand
from application.mediator.mediator import Mediator
from bot.keyboards.menu import MenuTextButtons, keyboard_menu
from bot.keyboards.tarif import BackMainMenu, TarifsTextButtons
from bot.texts.menu import MenuText



router = Router()


@router.message(F.text, Command("start"))
async def start(message: Message, mediator: Mediator):
    assert message.from_user.is_bot == False
    await mediator.handle_command(CreateUserCommand(
        tg_id=message.from_user.id,
        tg_username=message.from_user.username,
        is_premium=message.from_user.is_premium
    ))

    await message.answer(text=MenuText.DESCRIPTION, reply_markup=keyboard_menu())


@router.message(F.text, Command("menu"))
async def start(message: Message):
    await message.answer(text=MenuText.DESCRIPTION, reply_markup=keyboard_menu())



@router.message(F.text==BackMainMenu.BACK)
async def back_to_main_menu(message: Message):
    await message.answer(text='Меню', reply_markup=keyboard_menu())


@router.message(F.text==MenuTextButtons.TARIFS)
async def back_to_main_menu(message: Message):
    await message.answer(text='\n'.join(tarif.value for tarif in TarifsTextButtons), reply_markup=keyboard_menu())
