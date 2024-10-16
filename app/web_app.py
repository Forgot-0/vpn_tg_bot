from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from punq import Container

from application.commands.subscriptions.paid import PaidSubscriptionCommand
from application.mediator.mediator import Mediator
from bot.main import init_web_hook_bot
from infra.depends.init import get_mediator, init_container
from settings.config import Config


router = web.RouteTableDef()


@router.post('/paid')
async def paid(requests: web.Request):
    data = (await requests.json())
    mediator: Mediator = get_mediator()
    await mediator.handle_command(
        PaidSubscriptionCommand(
            tg_id=int(data['object']['metadata']['tg_id']),
            payment_id=data['object']['id'],
            subscription_id=data['object']['metadata']['subscription_id']
        )
    )
    return web.Response(text='OK')


def init_app():
    app = web.Application()
    container: Container = init_container()
    config: Config = container.resolve(Config)
    dp = container.resolve(Dispatcher)
    bot = container.resolve(Bot)

    rq_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    rq_handler.register(app, path=config.bot.path)

    app.add_routes(routes=router)
    setup_application(app, dp, bot=bot)
    web.run_app(app=app, host=config.webapp.host, port=config.webapp.port)




init_web_hook_bot()
init_app()