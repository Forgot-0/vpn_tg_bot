from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.dtos.users import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.subscriptions import SubscriptionRepository


@dataclass(frozen=True)
class GetSubscriptionQuery(BaseQuery):
    user_jwt_data: UserJWTData

    subscription_id: UUID


@dataclass(frozen=True)
class GetSubscriptionHandler(BaseQueryHandler[GetSubscriptionQuery, SubscriptionDTO]):
    subscription_repository: SubscriptionRepository

    async def handle(self, query: GetSubscriptionQuery) -> SubscriptionDTO:
        sub = await self.subscription_repository.get_by_id(query.subscription_id)

        if sub is None or (sub.user_id != query.user_jwt_data.id):
            raise

        return SubscriptionDTO.from_entity(sub)

