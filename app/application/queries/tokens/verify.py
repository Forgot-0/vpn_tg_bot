from dataclasses import dataclass

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.jwt_manager import JWTManager



@dataclass(frozen=True)
class VerifyTokenQuery(BaseQuery):
    token: str


@dataclass(frozen=True)
class VerifyTokenQueryHandler(BaseQueryHandler[VerifyTokenQuery, UserJWTData]):
    jwt_manager: JWTManager

    async def handle(self, query: VerifyTokenQuery) -> UserJWTData:
        token_data = await self.jwt_manager.validate_token(token=query.token)
        return UserJWTData.create_from_token(token_data)
