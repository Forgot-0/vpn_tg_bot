from dataclasses import dataclass

from application.dto.profile import ProfileDTO
from application.exeption import NotFoundActiveSubscriptionException
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.servers import BaseServerRepository
from domain.repositories.users import BaseUserRepository
from infrastructure.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class GetProfileVpnQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetProfileVpnQueryHandler(BaseQueryHandler[GetProfileVpnQuery, ProfileDTO]):
    user_repository: BaseUserRepository
    server_repository: BaseServerRepository
    vpn_server: BaseVpnService

    async def handle(self, query: GetProfileVpnQuery) -> ProfileDTO:
        user = await self.user_repository.get_by_id(id=query.user_id)
        server = await self.server_repository.get_by_id(server_id=user.server_id)
        profile = await self.vpn_server.get_by_id(id=user.uuid, server=server)
        if profile is None:
            raise NotFoundActiveSubscriptionException()
        return profile


