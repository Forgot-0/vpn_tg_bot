from dataclasses import dataclass

from application.dto.user import UserDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class GetByUserIdQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetByUserIdQueryHandler(BaseQueryHandler[GetByUserIdQuery, UserDTO]):
    user_repository: BaseUserRepository

    async def handle(self, query: GetByUserIdQuery) -> UserDTO:
        user = await self.user_repository.get_by_id(id=query.user_id)
        return UserDTO.from_entity(user=user)