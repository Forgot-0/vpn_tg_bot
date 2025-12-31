from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.servers.base import ServerDetailDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import NotFoundException
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetByIdServerQuery(BaseQuery):
    server_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetByIdServerQueryHandler(BaseQueryHandler[GetByIdServerQuery, ServerDetailDTO]):
    server_repository: BaseServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetByIdServerQuery) -> ServerDetailDTO:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        server = await self.server_repository.get_by_id(
            server_id=query.server_id
        )
        if server is None:
            raise NotFoundException()

        return ServerDetailDTO.from_entity(server)
