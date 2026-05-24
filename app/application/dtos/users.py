from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field

from app.domain.entities.user import User




class JwtTokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


@dataclass
class TokenPairDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    type: str
    sub: str
    jti: str
    did: str
    exp: float
    iat: float
    role: str


class UserJWTData(BaseModel):
    id: str
    role: str
    device_id: str | None = Field(default=None)

    @classmethod
    def create_from_token(cls, token_dto: Token) -> Self:
        return cls(
            id=token_dto.sub,
            role=token_dto.role,
            device_id=token_dto.did,
        )

    @classmethod
    def create_from_user(cls, user: User, device_id: str | None=None) -> Self:
        return cls(
            id=str(user.id),
            role=user.role.value,
            device_id=device_id
        )

    def to_dict(self) -> dict:
        return {
            "sub": self.id,
            "role": self.role,
            "did": self.device_id,
        }

