from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.application.dtos.base import BaseDTO
from app.domain.entities.user import User


@dataclass
class UserDTO(BaseDTO):
    id: UUID
    role: str
    email: str | None
    telegram_id: int | None
    referral_code: str
    referred_by: UUID | None
    referrals_count: int
    created_at: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)

    @classmethod
    def from_entity(cls, entity: User) -> Self:
        return cls(
            id=entity.id,
            role=entity.role.value,
            email=entity.email,
            telegram_id=entity.telegram_id,
            referral_code=entity.referral_code,
            referred_by=entity.referred_by,
            referrals_count=entity.referrals_count,
            created_at=entity.created_at,
        )


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

