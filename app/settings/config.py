from pydantic import Field
from pydantic_settings import BaseSettings


class BOT(BaseSettings):
    owner: int = Field(alias="OWNER")
    token: str = Field(alias='BOT_TOKEN')
    name: str = Field(alias="USERNAME_BOT")

    host: str = Field(alias='TELEGRAM_WEBHOOK_HOST')
    path: str = Field(alias='TELEGRAM_WEBHOOK_PATH')
    url: str = Field(alias='TELEGRAM_WEBHOOK_URL')

class YooKassaPayment(BaseSettings):
    account_id: str = Field(alias='PAYMENT_ID')
    secret_id: str = Field(alias='PAYMENT_SECRET')

class WebApp(BaseSettings):
    host: str = Field(alias='WEBAPP_WEBHOOK_HOST')
    port: int = Field(alias='WEBAPP_WEBHOOK_PORT')

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
    webapp = WebApp()
    yookass = YooKassaPayment()

settings = Config()