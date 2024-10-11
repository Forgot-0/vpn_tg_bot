from pydantic import Field
from pydantic_settings import BaseSettings


class BOT(BaseSettings):
    token: str = Field(alias='BOT_TOKEN')
    provider_token: str = Field(alias='PROVIDER_TOKEN')


class DataBase(BaseSettings):
    url: str = Field(alias='DATABASE_URL')
    username: str = Field(alias='DATABASE_USERNAME')
    password: str = Field(alias='DATABASE_PASSWORD')
    port: str = Field(alias='DATABASE_PORT')


class Broker(BaseSettings):
    url: str = Field(alias="BROKER_URL")


class VPN(BaseSettings):
    ip: str = Field(alias="VPN_IP")
    url: str = Field(alias="VPN_URL")
    pbk: str = Field(alias='VPN_PBK')
    urn_login: str = Field(alias='VPN_URL_LOGIN')
    urn_create: str = Field(alias='VPN_URL_CREATE')
    urn_delete: str = Field(alias='VPN_URL_DELETE', default="pass")
    urn_update: str = Field(alias='VPN_URL_UPDATE')
    urn_get: str = Field(alias='VPN_URL_GET')
    username: str = Field(alias='VPN_USERNAME')
    password: str = Field(alias='VPN_PASSWORD')
    secret: str = Field(alias='VPN_SECRET')


class Config:
    bot = BOT()
    broker = Broker()
    db = DataBase()
    vpn = VPN()


config = Config()