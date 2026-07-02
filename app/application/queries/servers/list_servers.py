from __future__ import annotations

from dataclasses import dataclass

from app.application.dtos.base import PaginatedResponseDTO
from app.application.dtos.servers import ServerDTO
from app.application.dtos.users import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.servers import ServerFilter, ServerRepository
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class ListServersQuery(BaseQuery):
    user_jwt_data: UserJWTData

    server_filter: ServerFilter


@dataclass(frozen=True)
class ListServersQueryHandler(BaseQueryHandler[ListServersQuery, PaginatedResponseDTO[ServerDTO]]):
    server_repository: ServerRepository
    access_service: RoleAccessControl

    async def handle(self, query: ListServersQuery) -> PaginatedResponseDTO[ServerDTO]:
        if not self.access_service.can_action(query.user_jwt_data.role, UserRole.ADMIN):
            raise 

        servers = await self.server_repository.list_filtered(filter=query.server_filter)

        return PaginatedResponseDTO(
            items=[ServerDTO.from_entity(server) for server in servers.items],
            total=servers.total,
            page=servers.page,
            page_size=servers.page_size
        )