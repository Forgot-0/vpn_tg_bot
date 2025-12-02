
from pydantic import BaseModel

from application.dtos.tokens.token import Token
from configs.app import app_settings
from domain.entities.user import User


class UserJWTData(BaseModel):
    id: str
    role: str

    @classmethod
    def create_from_user(cls, user: User) -> "UserJWTData":
        role = "admin" if app_settings.BOT_OWNER_ID == user.id else "user"

        return cls(
            id=str(user.id),
            role=role,
        )

    @classmethod
    def create_from_token(cls, token_dto: Token) -> "UserJWTData":
        return cls(
            id=token_dto.sub,
            role=token_dto.role,
        )

