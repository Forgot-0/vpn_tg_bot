from dataclasses import dataclass

from application.queries.base import BaseQuery, BaseQueryHandler
from domain.entities.subscription import Subscription
from domain.repositories.subscriptions import BaseSubscriptionRepository



@dataclass(frozen=True)
class GetListSubscriptionQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetListSubscriptionQueryHandler(BaseQueryHandler[GetListSubscriptionQuery, list[Subscription]]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetListSubscriptionQuery) -> list[Subscription]:
        subscriptions = await self.subscription_repository.get()
        return subscriptions