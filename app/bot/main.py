import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from redis.asyncio.client import Redis

from bot.middlewares.check_subs_channel import CheckSubsChannelMiddleware
from bot.middlewares.mediator import MediatorMiddleware
from domain.exception.base import ApplicationException
from configs.app import app_settings

from bot.handlers.start import router as start_router
from bot.handlers.subscription import router as subscription_router


logger = logging.getLogger(__name__)


async def startup_bot(bot: Bot):
    await bot.set_webhook(
        url=app_settings.webhook_url,
        drop_pending_updates=False,
        allowed_updates=["message", "inline_query", "callback_query"]
    )

def add_middlewares(dp: Dispatcher):
    dp.update.middleware(MediatorMiddleware())
    if app_settings.CHAT_TELEGRAM:
        dp.update.middleware(CheckSubsChannelMiddleware())

async def handle_exception(event: ErrorEvent):
    logger.error("Handle error", exc_info=event.exception, extra={"error": event.exception})
    if event.update.message:
        await event.update.message.answer(text=event.exception.message) # type: ignore
    else:
        await event.update.callback_query.message.answer(event.exception.message) # type: ignore

def init_dispatch() -> Dispatcher:
    dp = Dispatcher(storage=RedisStorage(Redis.from_url(app_settings.fsm_redis_url)))
    dp.startup.register(startup_bot)
    add_middlewares(dp=dp)
    dp.error.register(handle_exception, ExceptionTypeFilter(ApplicationException))

    dp.include_router(start_router)
    dp.include_router(subscription_router)
    return dp

def init_webhook(app: web.Application):
    bot = Bot(app_settings.BOT_TOKEN)
    dp = init_dispatch()
    rq_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    rq_handler.register(app, path=app_settings.TELEGRAM_WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
