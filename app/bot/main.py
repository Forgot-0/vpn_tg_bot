from aiogram import Bot, Dispatcher
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from bot.middlewares.mediator import MediatorMiddleware
from domain.exception.base import ApplicationException
from infrastructure.depends.init import init_container
from settings.config import settings

from bot.handlers.menu import router as menu_router
from bot.handlers.order import router as order_router
from bot.handlers.start import router as start_router
from bot.handlers.guide import router as guide_router
from bot.handlers.server import router as server_router
from bot.handlers.reward import router as reward_router
from bot.handlers.subscription import router as subscription_router



async def startup_bot(bot: Bot):
    await bot.set_webhook(
        url=settings.bot.url,
        drop_pending_updates=True,
        allowed_updates=["message", "inline_query", "callback_query"]
    )

def add_middlewares(dp: Dispatcher):
    dp.update.middleware(MediatorMiddleware())


async def handle_exception(event: ErrorEvent):
    await event.update.message.answer(text=event.exception.message)

def init_bot():
    container = init_container()

    dp: Dispatcher = container.resolve(Dispatcher)
    dp.startup.register(startup_bot)

    add_middlewares(dp=dp)

    dp.include_router(menu_router)
    dp.include_router(start_router)
    dp.include_router(order_router)
    dp.include_router(guide_router)
    dp.include_router(server_router)
    dp.include_router(reward_router)
    dp.include_router(subscription_router)

    dp.error.register(handle_exception, ExceptionTypeFilter(ApplicationException))

