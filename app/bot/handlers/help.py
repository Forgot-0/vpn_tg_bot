from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.help import help_keayboard
from bot.keyboards.menu import MenuTextButtons
from bot.texts.help import HelpText


router = Router()


@router.message(F.text==MenuTextButtons.HELP)
async def help(message: Message):
    await message.answer(text=HelpText.HELP, reply_markup=help_keayboard())