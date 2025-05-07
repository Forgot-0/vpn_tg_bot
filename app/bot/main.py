from aiogram import Bot, Dispatcher
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from bot.middlewares.mediator import MediatorMiddleware
from domain.exception.base import ApplicationException
from infrastructure.depends.init import init_container
from settings.config import settings


async def startup_bot(bot: Bot):
    await bot.set_webhook(
        url=settings.bot.url,
        drop_pending_updates=False,
        allowed_updates=["message", "inline_query", "callback_query"]
    )

def add_middlewares(dp: Dispatcher):
    dp.update.middleware(MediatorMiddleware())


async def handle_exception(event: ErrorEvent):
    if event.update.message:
        await event.update.message.answer(text=event.exception.message)
    else:
        await event.update.callback_query.message.answer(event.exception.message)


def init_dispatch() -> Dispatcher:
    container = init_container()

    dp: Dispatcher = container.resolve(Dispatcher)
    dp.startup.register(startup_bot)

    add_middlewares(dp=dp)

    dp.error.register(handle_exception, ExceptionTypeFilter(ApplicationException))

    return dp