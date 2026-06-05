from dataclasses import dataclass

from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.dtos.users import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.subscriptions import SubscriptionRepository


@dataclass(frozen=True)
class GetUserSubscriptionsQuery(BaseQuery):
    user_jwt_data: UserJWTData



@dataclass(frozen=True)
class GetUserSubscriptionsHandler(BaseQueryHandler[GetUserSubscriptionsQuery, list[SubscriptionDTO]]):
    subscription_repository: SubscriptionRepository

    async def handle(self, query: GetUserSubscriptionsQuery) -> list[SubscriptionDTO]:
        subs = await self.subscription_repository.list_by_user(query.user_jwt_data.id)
        return [SubscriptionDTO.from_entity(s) for s in subs]
