from dataclasses import dataclass

from application.dto.profile import Profile
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from infrastructure.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class GetByUserOrdersQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetByUserOrdersQueryHandler(BaseQueryHandler[GetByUserOrdersQuery, None]):
    vpn_service: BaseVpnService
    order_repository: BaseOrderRepository
    server_repository: BaseServerRepository

    async def handle(self, query: GetByUserOrdersQuery) -> list[Profile]:
        profiles = []
        orders = await self.order_repository.get_by_user_id(user_id=query.user_id)
        for order in orders:
            server = await self.server_repository.get_by_id(server_id=order.server_id)
            profiles.append(
                await self.vpn_service.get_by_id(id=order.id, server=server)
            )
        return profiles
            

