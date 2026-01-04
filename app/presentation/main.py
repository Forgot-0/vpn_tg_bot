import logging

from dishka.integrations.aiogram import setup_dishka as aiogram_setup_dishka
from dishka.integrations.fastapi import setup_dishka as fast_setup_dishka
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.bot.main import dp, bot
from app.configs.app import app_settings
from app.domain.exception.base import DomainException
from app.infrastructure.log.init import configure_logging
from app.presentation.exceptions import handle_domain_exeption, handle_uncown_exception, handle_validation_exeption
from app.presentation.init_data import init_data
from app.presentation.middlewares.context import set_request_id_middleware
from app.presentation.middlewares.structlog import structlog_bind_middleware
from app.presentation.webhooks.telegram import router as telegram_router
from app.presentation.webhooks.yookassa import router as yookassa_router
from app.presentation.routers.routers import router_v1
from app.setup.di.container import create_container



logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await dp.emit_startup(bot=bot, dispatcher=dp)
    await init_data(app.state.dishka_container)
    yield
    await dp.emit_shutdown(bot=bot, dispatcher=dp)
    await app.state.dishka_container.close()

def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[app_settings.WEB_APP_URL, ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
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
        openapi_url=(
            f"/api/v1/openapi.json"
            if app_settings.ENVIRONMENT in ["local", "testing"]
            else None
        ),
    )

    container = create_container()

    aiogram_setup_dishka(container=container, router=dp, auto_inject=True)
    fast_setup_dishka(app=app, container=container)

    setup_middlewares(app=app)
    setup_router(app=app)

    app.add_exception_handler(Exception, handle_uncown_exception)
    app.add_exception_handler(DomainException, handle_domain_exeption) # type: ignore
    app.add_exception_handler(RequestValidationError, handle_validation_exeption) # type: ignore


    return app

