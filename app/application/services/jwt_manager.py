from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from uuid import uuid4

from jose import ExpiredSignatureError, JWTError, jwt

from app.application.dtos.tokens.token import Token, TokenGroup, TokenType
from app.application.dtos.users.jwt import UserJWTData
from app.domain.services.utils import now_utc
from app.application.exception import ExpiredTokenException, InvalidTokenException


@dataclass
class JWTManager:
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


    def encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def decode(self, token: str) -> dict[str, Any]:
        try:
            data = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
        except ExpiredSignatureError as err:
            raise ExpiredTokenException(token=token) from err
        except JWTError as err:
            raise InvalidTokenException(token=token) from err
        return data

    def generate_payload(self, user_data: UserJWTData, token_type: TokenType) -> dict[str, Any]:
        now = now_utc()
        payload = {
            "type": token_type,
            "sub": user_data.id,
            "jti": str(uuid4()),
            "exp": (
                now + timedelta(minutes=self.access_token_expire_minutes)
                if token_type == TokenType.ACCESS
                else now + timedelta(days=self.refresh_token_expire_days)
            ).timestamp(),
            "iat": now.timestamp(),
        }
        if token_type == TokenType.ACCESS:
            payload["role"] = user_data.role

        return payload

    def create_token_pair(
        self,
        security_user: UserJWTData,
    ) -> TokenGroup:
        access_payload = self.generate_payload(
            security_user, TokenType.ACCESS
        )
        refresh_payload = self.generate_payload(
            security_user, TokenType.REFRESH
        )

        access_token = self.encode(access_payload)
        refresh_token = self.encode(refresh_payload)

        return TokenGroup(access_token=access_token, refresh_token=refresh_token)

    async def validate_token(self, token: str, token_type: TokenType=TokenType.ACCESS) -> Token:
        payload = self.decode(token)
        token_data = Token(**payload)

        if token_data.type != token_type:
            raise InvalidTokenException(token=token)

        return token_data

    async def refresh_tokens(self, refresh_token: str, security_user: UserJWTData) -> TokenGroup:
        token = await self.validate_token(refresh_token, token_type=TokenType.REFRESH)

        token_pair = self.create_token_pair(security_user=security_user)

        return token_pair
