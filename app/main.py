import asyncio
from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.main import init_dispatch
from configs.app import settings
from api.paid import router as paid_router



def bot_webhook():
    bot = Bot(settings.BOT_TOKEN)
    dp = init_dispatch()
    app = web.Application()

    rq_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    rq_handler.register(app, path=settings.TELEGRAM_WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.add_routes(routes=paid_router)
    web.run_app(app=app, host=settings.WEBAPP_WEBHOOK_HOST, port=settings.WEBAPP_WEBHOOK_PORT)


def bot_pool():
    bot = Bot(settings.BOT_TOKEN)
    dp = init_dispatch()
    asyncio.run(dp.start_polling(bot))


bot_webhook()