from dataclasses import dataclass

from application.dto.subscription import SubscriptionDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.entities.subscription import Subscription
from domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository



@dataclass(frozen=True)
class GetListSubscriptionQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetListSubscriptionQueryHandler(BaseQueryHandler[GetListSubscriptionQuery, list[SubscriptionDTO]]):
    subscription_repository: BaseSubscriptionRepository
    discount_repository: BaseDiscountRepository
    discount_user_repository: BaseDiscountUserRepository


    async def handle(self, query: GetListSubscriptionQuery) -> list[SubscriptionDTO]:

        subscriptions: set[Subscription] = set(await self.subscription_repository.get())
        discounts = await self.discount_repository.get()

        for discount in discounts:

            if discount.max_per_user:
                discount_user = await self.discount_user_repository.get_by_discount_user(
                    user_id=query.user_id,
                    discount_id=discount.id
                )

                if discount_user.count > discount.max_per_user:
                    continue

            if discount.subscription_ids:
                for subscription_id in discount.subscription_ids:
                    try:
                        subscriptions[subscription_id].set_discount(discount)
                    except:
                        ...
            else:
                for subscription in subscriptions:
                    subscription.set_discount(discount=discount)

        subs = [
            SubscriptionDTO.from_entity(sub)
            for sub in subscriptions
        ]


        return subs