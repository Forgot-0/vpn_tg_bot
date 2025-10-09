from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from dishka.integrations.aiogram import FromDishka

from application.commands.users.create import CreateUserCommand
from bot.messages.menu import AboutButton, AboutMessage, BackButton, HelpButton, HelpMessage, StartMessageBuilder
from infrastructure.mediator.base import BaseMediator


router = Router()


@router.message(Command("start"))
async def start(message: Message, mediator: FromDishka[BaseMediator]):
    data = StartMessageBuilder().build()
    data['photo'] = data.pop("media").media
    print(data['photo'])
    await message.answer_photo(**data)


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

@router.callback_query(F.data==BackButton.callback_data)
async def menu(callback_query: CallbackQuery, state: FSMContext):
    data = StartMessageBuilder().build()
    await callback_query.message.edit_media(**data)
    await state.clear()
    await callback_query.answer()


@router.callback_query(F.data==HelpButton.callback_data)
async def help(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(**HelpMessage().build())


@router.callback_query(F.data==AboutButton.callback_data)
async def about(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_media(**AboutMessage().build())
