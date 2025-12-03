
from pydantic import BaseModel

from app.application.dtos.tokens.token import Token
from app.configs.app import app_settings
from app.domain.entities.user import User


class UserJWTData(BaseModel):
    id: str
    role: str

    @classmethod
    def create_from_user(cls, user: User) -> "UserJWTData":
        role = "admin" if app_settings.BOT_OWNER_ID == user.telegram_id else "user"

        return cls(
            id=str(user.id.value),
            role=role,
        )

    @classmethod
    def create_from_token(cls, token_dto: Token) -> "UserJWTData":
        return cls(
            id=token_dto.sub,
            role=token_dto.role,
        )

