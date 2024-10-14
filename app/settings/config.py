from pydantic import Field
from pydantic_settings import BaseSettings


class BOT(BaseSettings):
    owner: int = Field(alias="OWNER")
    token: str = Field(alias='BOT_TOKEN')
    provider_token: str = Field(alias='PROVIDER_TOKEN')

    host: str = Field(alias='TELEGRAM_WEBHOOK_HOST')
    urn: str = Field(alias='TELEGRAM_WEBHOOK_PATH')

class DataBase(BaseSettings):
    url: str = Field(alias='DATABASE_URL')
    username: str = Field(alias='DATABASE_USERNAME')
    password: str = Field(alias='DATABASE_PASSWORD')
    port: str = Field(alias='DATABASE_PORT')


class Broker(BaseSettings):
    url: str = Field(alias="BROKER_URL")


class VPN(BaseSettings):
    username: str = Field(alias='VPN_USERNAME')
    password: str = Field(alias='VPN_PASSWORD')
    secret: str = Field(alias='VPN_SECRET')


class Config:
    bot = BOT()
    broker = Broker()
    db = DataBase()
    vpn = VPN()

