

from pydantic import BaseModel, Field


class Create3XUISerrverRequest(BaseModel):
    limit: int
    region_code: str

    ip: str
    panel_port: int
    panel_path: str
    domain: str | None

    username: str
    password: str
    twoFactorCode: str | None = Field(default=None)
