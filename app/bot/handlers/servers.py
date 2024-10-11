
from aiogram import F, Router
from aiogram.types import Message

from application.commands.servers.create import CreateServerCommand
from application.mediator.mediator import Mediator


router = Router()


@router.message(F.text)
async def create_server(message: Message, mediator: Mediator):
    await mediator.handle_command(
        CreateServerCommand(text=message.text)
    )