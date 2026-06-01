from dataclasses import dataclass

from app.application.dtos.users import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.servers import VPNServerRepository
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetActiveServersQuery(BaseQuery):
    user_jwt_data: UserJWTData



@dataclass(frozen=True)
class GetActiveServersQueryHandler(BaseQueryHandler[GetActiveServersQuery, None]):
    server_repository: VPNServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetActiveServersQuery) -> None:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise


        actives = await self.server_repository.list_active()

