from aiohttp.web import Application

from bot.main import init_web_hook_bot
from infra.depends.init import init_container
from settings.config import Config



async def factory_app() -> Application:
    app = Application()
    config: Config = init_container().resolve(Config)

    app.router.add_route(
        "*",
        path=config.bot.urn,
        handler=await init_web_hook_bot(),
        name='telegram_handler'
    )
    return app