from aiogram import Bot, Dispatcher
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.fsm.storage.memory import MemoryStorage

from bot.middlewares.check_subs_channel import CheckSubsChannelMiddleware
from bot.middlewares.mediator import MediatorMiddleware
from domain.exception.base import ApplicationException
from configs.app import settings

from bot.handlers.start import router as start_router

async def startup_bot(bot: Bot):
    await bot.set_webhook(
        url=settings.webhook_url,
        drop_pending_updates=False,
        allowed_updates=["message", "inline_query", "callback_query"]
    )

def add_middlewares(dp: Dispatcher):
    dp.update.middleware(MediatorMiddleware())
    dp.update.middleware(CheckSubsChannelMiddleware())

async def handle_exception(event: ErrorEvent):
    if event.update.message:
        await event.update.message.answer(text=event.exception.message) # type: ignore
    else:
        await event.update.callback_query.message.answer(event.exception.message) # type: ignore


def init_dispatch() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(startup_bot)

    add_middlewares(dp=dp)

    dp.error.register(handle_exception, ExceptionTypeFilter(ApplicationException))

    dp.include_router(start_router)
    return dp