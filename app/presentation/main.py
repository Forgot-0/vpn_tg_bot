import logging
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn

from bot.main import dp, bot
from configs.app import app_settings
from presentation.webhooks.telegram import router as telegram_router
from presentation.webhooks.yookassa import router as yookassa_router


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await dp.emit_startup(bot=bot)
    yield
    await dp.emit_shutdown(bot=bot)


def init_api() -> FastAPI:
    logger.debug("Initialize API")
    app = FastAPI(
        title='Simple subscription',
        docs_url='/api/docs',
        description='Simple subscription + DDD, CQRS',
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(telegram_router)
    app.include_router(yookassa_router)

    return app


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host=app_settings.WEBAPP_WEBHOOK_HOST,
        port=app_settings.WEBAPP_WEBHOOK_PORT,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Running API")
    await server.serve()