from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.entities.discount import DiscountUser
from domain.events.orders.paid import PaidOrderEvent
from domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository
from domain.repositories.orders import BaseOrderRepository


@dataclass(frozen=True)
class UsedDiscountEventHandler(BaseEventHandler[PaidOrderEvent, None]):
    order_repository: BaseOrderRepository
    discount_user_repository: BaseDiscountUserRepository
    discount_repository: BaseDiscountRepository

    async def handle(self, event: PaidOrderEvent) -> None:
        order = await self.order_repository.get_by_id(id=event.order_id)
        if order.discount:
            await self.discount_user_repository.incr_count(
                user_id=order.user_id,
                discount_id=order.discount.id,
                incr=1
            )