from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from punq import Container

from bot.handlers.guide import router as guide_router
from bot.handlers.menu import router as menu_router
from bot.handlers.subscriptions import router as sub_router
from bot.handlers.servers import init_router as init_server_router

from bot.middlewares.mediator import MediatorMiddleware
from infra.depends.init import init_container
from settings.config import Config



async def set_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command='/menu', description="Меню"),
            BotCommand(command='/get_active_vpn_url', description="Получить все активные ссылки")
        ]
    )


async def set_routers(dp: Dispatcher, container: Container):
    dp.include_router(guide_router)
    dp.include_router(menu_router)
    dp.include_router(sub_router)
    dp.include_router(init_server_router(config=container.resolve(Config)))


async def add_middlewares(dp: Dispatcher):
    dp.update.middleware(MediatorMiddleware())


async def init_bot():
    container: Container = init_container()

    bot: Bot = container.resolve(Bot)
    dp: Dispatcher = Dispatcher()
    await set_commands(bot=bot)
    await set_routers(dp=dp, container=container)
    await add_middlewares(dp=dp)

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


async def init_web_hook_bot():
    container: Container = init_container()
    config: Config = container.resolve(Config)

    bot: Bot = container.resolve(Bot)
    await bot.set_webhook(
        config.bot.urn
    )

    dp: Dispatcher = Dispatcher()

    await set_commands(bot=bot)
    await set_routers(dp=dp, container=container)
    await add_middlewares(dp=dp)

    return SimpleRequestHandler(dispatcher=dp, bot=bot)