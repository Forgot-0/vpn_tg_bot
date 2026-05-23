from typing import Annotated, ClassVar, Literal
from pydantic import BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
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
    BACKEND_CORS_ORIGINS: ClassVar[Annotated[list[str] | str, BeforeValidator(BaseConfig.parse_list)]] = []

    PAYMENT_SECRET: str = ""
    PAYMENT_ID: int = 0

    @computed_field
    @property
    def web_app_url(self) -> str:
        return f"https://{self.DOMAIN}"

    @computed_field
    @property
    def webhook_url(self) -> str:
        if self.ENVIRONMENT in ["local", "testing"]:
            return f"https://{self.DOMAIN}{self.TELEGRAM_WEBHOOK_PATH}"
        return f"https://api.{self.DOMAIN}{self.TELEGRAM_WEBHOOK_PATH}"

    APP_PORT: int = 8080
    APP_HOST: str = "0.0.0.0"

    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    SQL_ECHO: bool = False

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ) # type: ignore

    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    @computed_field
    @property
    def redis_url(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

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


app_config = AppConfig()
