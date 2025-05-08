from typing import Annotated, Literal
from pydantic import BeforeValidator, computed_field
from configs.base import BaseConfig


class AppConfig(BaseConfig):
    ENVIRONMENT: Literal['local', 'production', 'testing'] = 'local'

    BOT_TOKEN: str = ""
    BOT_OWNER_ID: int = 0
    BOT_USERNAME: str = ""
    
    TELEGRAM_WEBHOOK_DOMAIN: str = ""
    TELEGRAM_WEBHOOK_PATH: str = "/webhook"

    @computed_field
    @property
    def webhook_url(self) -> str:
        return f"https://{self.TELEGRAM_WEBHOOK_DOMAIN}{self.TELEGRAM_WEBHOOK_PATH}"


    PAYMENT_SECRET: str = ""
    PAYMENT_ID: int = 0

    WEBAPP_WEBHOOK_PORT: int = 8080
    WEBAPP_WEBHOOK_HOST: str = "0.0.0.0"

    DATABASE_DB: str = ""
    DATABASE_USERNAME: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_PORT: int = 27017

    @computed_field
    @property
    def mongo_url(self) -> str:
        return f"mongodb://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@mongo:{self.DATABASE_PORT}/"

    BROKER_URL: str = ""

    VPN_USERNAME: str = ""
    VPN_PASSWORD: str = ""
    VPN_SECRET: str = ""


    LOG_LEVEL: str = 'ERROR'
    LOG_HANDLERS: Annotated[list[Literal['stream', 'file']] | str, BeforeValidator(BaseConfig.parse_list)] = ['stream']

settings = AppConfig()