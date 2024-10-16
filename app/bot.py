import asyncio
from aiogram import Bot, Dispatcher
from punq import Container

from bot.main import add_middlewares, set_routers
from infra.depends.init import init_container
from settings.config import Config



async def init_web_hook_bot():
    container: Container = init_container()
    config: Config = container.resolve(Config)
    bot: Bot = container.resolve(Bot)
    await bot.delete_webhook(drop_pending_updates=False)
    dp: Dispatcher = container.resolve(Dispatcher)
    set_routers(dp=dp, container=container)
    add_middlewares(dp=dp)
    await dp.start_polling(bot)


asyncio.run(init_web_hook_bot())