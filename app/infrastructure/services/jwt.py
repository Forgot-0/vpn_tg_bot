from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from uuid import uuid4

import jwt

from app.application.dtos.users import JwtTokenType, Token, TokenGroup, UserJWTData
from app.application.interfaces.auth import JWTManager
from app.configs.app import app_config
from app.domain.services.clock import now_utc



@dataclass
class IJWTService(JWTManager):
    def create_token_pair(
        self,
        security_user: UserJWTData,
    ) -> TokenGroup:
        access_payload = self.generate_payload(
            security_user, JwtTokenType.ACCESS
        )
        refresh_payload = self.generate_payload(
            security_user, JwtTokenType.REFRESH
        )

        access_token = self.encode(access_payload)
        refresh_token = self.encode(refresh_payload)

        return TokenGroup(access_token=access_token, refresh_token=refresh_token)

    def generate_payload(self, user_data: UserJWTData, token_type: JwtTokenType) -> dict[str, Any]:
        now = now_utc()
        payload = {
            "type": token_type,
            "sub": user_data.id,
            "did": user_data.device_id,
            "jti": str(uuid4()),
            "exp": (
                now + timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
                if token_type == JwtTokenType.ACCESS
                else now + timedelta(days=app_config.REFRESH_TOKEN_EXPIRE_DAYS)
            ).timestamp(),
            "iat": now.timestamp(),
        }
        if token_type == JwtTokenType.ACCESS:
            payload["role"] = user_data.role

        return payload

    def encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, app_config.JWT_SECRET_KEY, algorithm=app_config.JWT_ALGORITHM)

    def decode(self, token: str) -> dict[str, Any]:
        try:
            data = jwt.decode(token, app_config.JWT_SECRET_KEY, algorithms=[app_config.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError as err:
            raise 
        except jwt.PyJWTError as err:
            raise 
        return data

    async def validate_token(self, token: str, token_type: JwtTokenType=JwtTokenType.ACCESS) -> Token:
        payload = self.decode(token)
        token_data = Token(**payload)

        if token_data.type != token_type:
            raise

        return token_data

