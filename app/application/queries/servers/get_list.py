from dataclasses import dataclass

from app.application.dtos.base import PaginatedResponseDto
from app.application.dtos.servers.base import ServerDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.filters.server import ServerFilter
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetListServerQuery(BaseQuery):
    server_query: ServerFilter
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetListServerQueryHandler(BaseQueryHandler[GetListServerQuery, PaginatedResponseDto[ServerDTO]]):
    server_repository: BaseServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetListServerQuery) -> PaginatedResponseDto[ServerDTO]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        result = await self.server_repository.find_by_filter(query.server_query)
        return PaginatedResponseDto(
            items=[ServerDTO.from_entity(user) for user in result.items],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_previous=result.has_previous,
            next_page=result.next_page,
            previous_page=result.previous_page
        )
