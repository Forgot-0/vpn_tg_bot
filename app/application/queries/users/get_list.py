from dataclasses import dataclass

from app.application.dtos.base import PaginatedResponseDto
from app.application.dtos.users.base import UserDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.filters.user import UserFilter
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetListUserQuery(BaseQuery):
    user_query: UserFilter
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetListUserQueryHandler(BaseQueryHandler[GetListUserQuery, PaginatedResponseDto[UserDTO]]):
    user_repository: BaseUserRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetListUserQuery) -> PaginatedResponseDto[UserDTO]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        result = await self.user_repository.find_by_filter(query.user_query)

        return PaginatedResponseDto(
            items=[UserDTO.from_entity(user) for user in result.items],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_previous=result.has_previous,
            next_page=result.next_page,
            previous_page=result.previous_page
        )
