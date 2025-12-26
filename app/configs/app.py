from typing import Annotated, ClassVar, Literal
from pydantic import BeforeValidator, computed_field
from app.configs.base import BaseConfig


class AppConfig(BaseConfig):
    ENVIRONMENT: Literal['local', 'production', 'testing'] = 'local'

    SECRET: str = ""

    WEBHOOK_SECRET: str = ""

    BOT_TOKEN: str = ""
    BOT_OWNER_ID: int = 0
    BOT_USERNAME: str = ""

    CHAT_TELEGRAM: int = 0

    VPN_HELP_ACCOUNT: str = ""

    DOMAIN: str = ""
    TELEGRAM_WEBHOOK_PATH: str = "/webhook"

    BACKEND_CORS_ORIGINS: Annotated[list[str] | str, BeforeValidator(BaseConfig.parse_list)] = []

    @computed_field
    @property
    def webhook_url(self) -> str:
        return f"https://{self.DOMAIN}{self.TELEGRAM_WEBHOOK_PATH}"

    PAYMENT_SECRET: str = ""
    PAYMENT_ID: int = 0

    WEBAPP_WEBHOOK_PORT: int = 8080
    WEBAPP_WEBHOOK_HOST: str = "0.0.0.0"

    DATABASE_DB: str = ""
    DATABASE_USERNAME: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_PORT: int = 27017
    DATABASE_HOST: str = "mongo"

    @computed_field
    @property
    def mongo_url(self) -> str:
        return f"mongodb://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/"

    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    @computed_field
    @property
    def fsm_redis_url(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1'

    LOG_LEVEL: str = 'ERROR'
    JSON_LOG: bool = True
    PATH_LOG: str | None = ".logs/logs.log"
    LOG_HANDLERS: Annotated[list[Literal['stream', 'file']] | str, BeforeValidator(BaseConfig.parse_list)] = ['stream']


    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"


app_settings = AppConfig()