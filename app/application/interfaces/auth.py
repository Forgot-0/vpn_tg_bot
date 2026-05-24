from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol

from app.application.dtos.users import JwtTokenType, Token, UserJWTData


@dataclass
class JWTService(Protocol):
    def generate_payload(self, user_data: UserJWTData, token_type: JwtTokenType) -> dict[str, Any]:
        ...

    def encode(self, payload: dict[str, Any]) -> str:
        ...

    def decode(self, token: str) -> dict[str, Any]:
        ...

    async def validate_token(self, token: str, token_type: JwtTokenType=JwtTokenType.ACCESS) -> Token:
        ...
