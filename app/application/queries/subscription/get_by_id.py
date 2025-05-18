from dataclasses import dataclass
from uuid import UUID

from application.dtos.subsciprions.subscription import SubscriptionDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.values.subscriptions import SubscriptionId


@dataclass(frozen=True)
class GetByIdQuery(BaseQuery):
    subscription_id: UUID


@dataclass(frozen=True)
class GetByIdQueryHandler(BaseQueryHandler[GetByIdQuery, SubscriptionDTO]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetByIdQuery) -> SubscriptionDTO:
        subscription = await self.subscription_repository.get_by_id(SubscriptionId(query.subscription_id))

        if not subscription:
            raise

        return SubscriptionDTO.from_entity(subscription)

