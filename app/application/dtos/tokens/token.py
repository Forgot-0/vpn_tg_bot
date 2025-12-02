from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"



class TokenGroup(BaseModel):
    refresh_token: str
    access_token: str


class Token(BaseModel):
    type: str
    sub: str
    jti: str
    exp: float
    iat: float
    role: str = Field(default="user")

