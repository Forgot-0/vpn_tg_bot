from dataclasses import dataclass

from app.domain.entities.subscription import Subscription
from app.domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository


@dataclass
class DiscountService:
    discount_repository: BaseDiscountRepository
    discount_user_repository: BaseDiscountUserRepository

    async def set_discounts(self, user_id: int, subscriptions: list[Subscription]) -> None:
        discounts = await self.discount_repository.get()

        if discounts:
            for discount in discounts:
                if not discount.is_valid():
                    continue

                if discount.conditions.get('max_per_user'):
                    discount_user = await self.discount_user_repository.get_by_discount_user(
                        user_id=user_id,
                        discount_id=discount.id
                    )
                    if discount_user is not None and discount_user.count >= discount.conditions['max_per_user']:
                        continue

                if discount.conditions.get('subscription_ids'):
                    for subscription_id in discount.conditions['subscription_ids']:
                        try:
                            index_subs = subscriptions.index(subscription_id)
                            subscriptions[index_subs].set_discount(discount=discount)
                        except Exception as ex:
                            ...
                else:
                    for subscription in subscriptions:
                        subscription.set_discount(discount=discount)

    async def set_on_order_discount(self, user_id: int, subscription: Subscription) -> None:
        ...