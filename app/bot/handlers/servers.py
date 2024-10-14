
from aiogram import F, Router
from aiogram.types import Message

from application.commands.servers.create import CreateServerCommand
from application.mediator.mediator import Mediator
from settings.config import Config






async def create_server(message: Message, mediator: Mediator):
    await mediator.handle_command(
        CreateServerCommand(text=message.text)
    )




def init_router(config: Config) -> Router:
    router = Router()
    router.message.register(create_server, F.text.startswith('{"ip":'), F.from_user.id==config.bot.owner)


    return router