from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.users import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.servers import VPNServerRepository
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class VPNServerInfo:
    id: UUID
    name: str
    region_code: str
    is_active: bool
    current_clients: int
    max_clients: int | None
    supported_protocols: list[str]


@dataclass(frozen=True)
class GetActiveServersQuery(BaseQuery):
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetActiveServersQueryHandler(BaseQueryHandler[GetActiveServersQuery, list[VPNServerInfo]]):
    server_repository: VPNServerRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetActiveServersQuery) -> list[VPNServerInfo]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise

        servers = await self.server_repository.list_active()

        return [
            VPNServerInfo(
                id=server.id,
                name=server.name,
                region_code=server.region_code,
                is_active=server.is_active,
                current_clients=server.current_clients,
                max_clients=server.max_clients,
                supported_protocols=[p.value for p in server.supported_protocols],
            )
            for server in servers
        ]