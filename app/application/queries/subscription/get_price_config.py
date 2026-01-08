from dataclasses import dataclass

from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.entities.price import PriceConfig
from app.domain.repositories.price import BasePriceRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetPriceConfigQuery(BaseQuery):
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetPriceConfigQueryHandler(BaseQueryHandler[GetPriceConfigQuery, PriceConfig]):
    price_repository: BasePriceRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetPriceConfigQuery) -> PriceConfig:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()
        cfg = await self.price_repository.get_price_config()
        return cfg
