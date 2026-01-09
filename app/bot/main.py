import logging


from aiogram import Bot, Dispatcher
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramAPIError

from app.bot.middlewares.check_subs_channel import CheckSubsChannelMiddleware
from app.bot.static.init import photo_manager
from app.domain.exception.base import DomainException
from app.configs.app import app_settings

from app.bot.handlers.start import router as start_router
from app.bot.handlers.subscription import router as subscription_router


logger = logging.getLogger(__name__)


async def startup_bot(bot: Bot) -> None:
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="🖥 Web",
            web_app=WebAppInfo(
                url=app_settings.web_app_url
            )
        )
    )
    if (await bot.get_webhook_info()).url != app_settings.webhook_url:
        await bot.delete_webhook(drop_pending_updates=False)
        await bot.set_webhook(
            url=app_settings.webhook_url,
            drop_pending_updates=False,
            allowed_updates=["message", "inline_query", "callback_query"],
            secret_token=app_settings.WEBHOOK_SECRET
            )
    await photo_manager.init_photo(bot)


async def shutdown_bot(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=False)


def add_middlewares(dp: Dispatcher):

    if app_settings.CHAT_TELEGRAM:
        dp.update.middleware(CheckSubsChannelMiddleware())

async def handle_domain_exception(event: ErrorEvent):
    logger.error("Handle error", exc_info=event.exception, extra={"error": event.exception.message}) # type: ignore

async def handler_telegram_exception(event: ErrorEvent) -> None:
    logger.error("Telegram api error", exc_info=event.exception, extra={
        "error": str(event.exception), "event": event.update.model_dump()
    })


def init_dispatch() -> Dispatcher:
    dp = Dispatcher(storage=RedisStorage.from_url(app_settings.fsm_redis_url))
    dp.startup.register(startup_bot)
    dp.shutdown.register(shutdown_bot)
    add_middlewares(dp=dp)
    dp.error.register(handle_domain_exception, ExceptionTypeFilter(DomainException))
    dp.error.register(handler_telegram_exception, ExceptionTypeFilter(TelegramAPIError))

    dp.include_router(start_router)
    dp.include_router(subscription_router)
    return dp

def init_bot() -> Bot:
    return Bot(app_settings.BOT_TOKEN)


bot = init_bot()
dp = init_dispatch()
