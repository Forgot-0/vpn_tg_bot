from pydantic import BaseModel, Field



class Client(BaseModel):
    id: str
    email: str
    expiryTime: int
    tg_id: int
    flow: str = "xtls-rprx-vision"
    enable: bool = True
    limitIp: int = 0


class Settings(BaseModel):
    clients: list[Client]


class CreateVpnUrl(BaseModel):
    id: int = Field(default=1)
    settings: Settings



