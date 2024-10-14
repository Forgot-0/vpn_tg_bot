from dataclasses import dataclass

from application.queries.base import BaseQuery, BaseQueryHandler
from domain.entities.subscription import Subscription
from infra.repositories.subscriptions.base import BaseSubscriptionRepository



@dataclass(frozen=True)
class GetAllActiveSubsQuery(BaseQuery):
    tg_id: int


@dataclass(frozen=True)
class GetAllActiveSubsQueryHandler(BaseQueryHandler[GetAllActiveSubsQuery, list[Subscription]]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetAllActiveSubsQuery) -> list[Subscription]:
        subscriptions = await self.subscription_repository.get_active_subscription(tg_id=query.tg_id)
        return subscriptions