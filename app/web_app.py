import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from punq import Container

from bot.main import init_web_hook_bot
from infra.depends.init import init_container
from settings.config import Config



def init_app():
    app = web.Application()
    container: Container = init_container()
    config: Config = container.resolve(Config)
    dp = container.resolve(Dispatcher)
    bot = container.resolve(Bot)

    rq_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    rq_handler.register(app, path=config.bot.path)

    setup_application(app, dp, bot=bot)
    web.run_app(app=app, host=config.webapp.host, port=config.webapp.port)




init_web_hook_bot()
init_app()