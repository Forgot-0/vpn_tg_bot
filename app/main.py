from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from punq import Container

from bot.main import init_bot
from infrastructure.depends.init import init_container
from settings.config import Config
from api.paid import router as paid_router




def init_app():
    init_bot()

    app = web.Application()

    container: Container = init_container()
    config: Config = container.resolve(Config)

    dp = container.resolve(Dispatcher)
    bot = container.resolve(Bot)
    rq_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    rq_handler.register(app, path=config.bot.path)
    setup_application(app, dp, bot=bot)

    app.add_routes(routes=paid_router)
    web.run_app(app=app, host=config.webapp.host, port=config.webapp.port)


init_app()