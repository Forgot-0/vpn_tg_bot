from dataclasses import dataclass

from app.application.dtos.base import PaginatedResult
from app.application.dtos.subscriptions.subscription import SubscriptionDTO, SubscriptionListParams
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetListSubscriptionsQuery(BaseQuery):
    subscription_query: SubscriptionListParams
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetListSubscriptionsQueryHandler(BaseQueryHandler[GetListSubscriptionsQuery, PaginatedResult[SubscriptionDTO]]):
    subscription_repository: BaseSubscriptionRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetListSubscriptionsQuery) -> PaginatedResult[SubscriptionDTO]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        result = await self.subscription_repository.get_list(query.subscription_query)
        return PaginatedResult(
            items=[SubscriptionDTO.from_entity(user) for user in result.items],
            pagination=result.pagination
        )
