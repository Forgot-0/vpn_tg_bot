from dataclasses import dataclass

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class GetUserByTgIdQuery(BaseQuery):
    telegram_id: int


@dataclass(frozen=True)
class GetUserByTgIdQueryHandler(BaseQueryHandler[GetUserByTgIdQuery, UserJWTData]):
    user_repository: BaseUserRepository

    async def handle(self, query: GetUserByTgIdQuery) -> UserJWTData:
       user = await self.user_repository.get_by_telegram_id(query.telegram_id)
       if user is None:
           raise
       return UserJWTData.create_from_user(user)
