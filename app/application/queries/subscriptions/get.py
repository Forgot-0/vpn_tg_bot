from dataclasses import dataclass

from application.dto.subscription import SubscriptionDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.entities.subscription import Subscription
from domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.services.discounts import DiscountService



@dataclass(frozen=True)
class GetListSubscriptionQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetListSubscriptionQueryHandler(BaseQueryHandler[GetListSubscriptionQuery, list[SubscriptionDTO]]):
    subscription_repository: BaseSubscriptionRepository
    discount_service: DiscountService

    async def handle(self, query: GetListSubscriptionQuery) -> list[SubscriptionDTO]:

        subscriptions: list[Subscription] = await self.subscription_repository.get()
        
        await self.discount_service.set_discounts(user_id=query.user_id, subscriptions=subscriptions)

        subs = [
            SubscriptionDTO.from_entity(sub)
            for sub in subscriptions
        ]


        return subs