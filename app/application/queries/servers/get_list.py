from dataclasses import dataclass

from app.application.dtos.base import PaginatedResult
from app.application.dtos.servers.base import ServerDTO, ServerListParams
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetListServerQuery(BaseQuery):
    server_query: ServerListParams
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetListServerQueryHandler(BaseQueryHandler[GetListServerQuery, PaginatedResult[ServerDTO]]):
    server_repository: BaseServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetListServerQuery) -> PaginatedResult[ServerDTO]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        result = await self.server_repository.get_list(query.server_query)
        return PaginatedResult(
            items=[ServerDTO.from_entity(user) for user in result.items],
            pagination=result.pagination
        )
