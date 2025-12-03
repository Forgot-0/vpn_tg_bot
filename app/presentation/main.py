import logging

from dishka.integrations.aiogram import setup_dishka as aiogram_setup_dishka
from dishka.integrations.fastapi import setup_dishka as fast_setup_dishka
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware

from bot.main import dp, bot
from configs.app import app_settings
from infrastructure.di.container import create_container
from infrastructure.log.init import configure_logging
from presentation.middlewares.context import set_request_id_middleware
from presentation.middlewares.structlog import structlog_bind_middleware
from presentation.webhooks.telegram import router as telegram_router
from presentation.webhooks.yookassa import router as yookassa_router
from presentation.routers.routers import router_v1

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await dp.emit_startup(bot=bot, dispatcher=dp)
    yield
    await dp.emit_shutdown(bot=bot, dispatcher=dp)
    await app.state.dishka_container.close()

def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=structlog_bind_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)


def setup_router(app: FastAPI) -> None:
    app.include_router(telegram_router)
    app.include_router(yookassa_router)
    app.include_router(router_v1, prefix="/api/v1")


def init_api() -> FastAPI:
    configure_logging()
    logger.debug("Initialize API")
    app = FastAPI(
        title='Simple subscription',
        docs_url='/api/docs',
        description='Simple subscription + DDD, CQRS',
        lifespan=lifespan,
    )

    container = create_container()
    aiogram_setup_dishka(container=container, router=dp, auto_inject=True)
    fast_setup_dishka(app=app, container=container)

    setup_middlewares(app=app)
    setup_router(app=app)

    return app


