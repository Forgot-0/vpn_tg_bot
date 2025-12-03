from dataclasses import dataclass

from app.application.dtos.base import PaginatedResult
from app.application.dtos.users.base import UserDTO, UserListParams
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class GetListUserQuery(BaseQuery):
    user_query: UserListParams
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetListUserQueryHandler(BaseQueryHandler[GetListUserQuery, PaginatedResult[UserDTO]]):
    user_repository: BaseUserRepository

    async def handle(self, query: GetListUserQuery) -> PaginatedResult[UserDTO]:
        if query.user_jwt_data.role != "admin":
            raise

        result = await self.user_repository.get_list(query.user_query)
        return PaginatedResult(
            items=[UserDTO.from_entity(user) for user in result.items],
            pagination=result.pagination
        )