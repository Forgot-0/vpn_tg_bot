import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from punq import Container

from bot.deepends import create_indexes
from bot.handlers.guide import router as guide_router
from bot.handlers.help import router as help_router
from bot.handlers.menu import router as menu_router
from bot.handlers.servers import init_router as init_server_router
from bot.handlers.subscriptions import router as sub_router


from bot.middlewares.mediator import MediatorMiddleware
from infra.depends.init import init_container
from infra.repositories.users.base import BaseUserRepository
from settings.config import Config



async def set_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command='/menu', description="Меню"),
            BotCommand(command='/get_active_vpn_url', description="Получить все активные ссылки")
        ]
    )


def set_routers(dp: Dispatcher, container: Container):
    dp.include_router(guide_router)
    dp.include_router(menu_router)
    dp.include_router(help_router)
    dp.include_router(sub_router)

    dp.include_router(init_server_router(config=container.resolve(Config)))


def add_middlewares(dp: Dispatcher):
    dp.update.middleware(MediatorMiddleware())


async def on_startup(bot: Bot):
    await bot.set_webhook(init_container().resolve(Config).bot.url, drop_pending_updates=True)
    await create_indexes()


def init_web_hook_bot():
    container: Container = init_container()
    config: Config = container.resolve(Config)
    bot: Bot = container.resolve(Bot)

    dp: Dispatcher = container.resolve(Dispatcher)
    dp.startup.register(on_startup)
    set_routers(dp=dp, container=container)
    add_middlewares(dp=dp)
