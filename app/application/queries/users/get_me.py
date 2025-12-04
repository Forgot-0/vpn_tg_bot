from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.base import PaginatedResult
from app.application.dtos.users.base import UserDTO, UserListParams
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId


@dataclass(frozen=True)
class GetMeUserQuery(BaseQuery):
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetMeUserQueryHandler(BaseQueryHandler[GetMeUserQuery, PaginatedResult[UserDTO]]):
    user_repository: BaseUserRepository

    async def handle(self, query: GetMeUserQuery) -> UserDTO:
        user = await self.user_repository.get_by_id(id=UserId(UUID(query.user_jwt_data.id)))
        if user is None:
            raise
        return UserDTO.from_entity(user)
