
from aiogram import F, Router
from aiogram.types import Message

from application.commands.servers.create import CreateServerCommand
from application.commands.servers.delete_not_active_user import DeletNotActiveUserCommand
from application.mediator.mediator import Mediator
from settings.config import settings


router = Router()


@router.message(
        F.text.startswith('{"ip":'),
        F.from_user.id==settings.bot.owner
    )
async def create_server(message: Message, mediator: Mediator):
    await mediator.handle_command(
        CreateServerCommand(text=message.text)
    )

@router.message(
        F.text=='/delete_not_active_user',
        F.from_user.id==settings.bot.owner
    )
async def delete_not_active_user(message: Message, mediator: Mediator):
    await mediator.handle_command(DeletNotActiveUserCommand())
    await message.answer('Success')

