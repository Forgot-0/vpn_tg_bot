from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.users.base import UserDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import NotFoundException
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId, UserRole


@dataclass(frozen=True)
class GetByIdUserQuery(BaseQuery):
    user_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetByIdUserQueryHandler(BaseQueryHandler[GetByIdUserQuery, UserDTO]):
    user_repository: BaseUserRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetByIdUserQuery) -> UserDTO:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ) or UUID(query.user_jwt_data.id) != query.user_id: raise

        user = await self.user_repository.get_by_id(
            UserId(query.user_id)
        )
        if user is None:
            raise NotFoundException()

        return UserDTO.from_entity(user)
