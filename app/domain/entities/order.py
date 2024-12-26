from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.entities.discount import Discount
from domain.entities.subscription import Subscription
from domain.events.orders.paid import PaidOrderEvent



@dataclass
class Order(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    subscription: Subscription
    user_id: int
    server_id: UUID

    total_price: float

    payment_date: datetime | None = field(default=None, kw_only=True)
    payment_id: UUID | None = field(default=None, kw_only=True)
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    discount: Discount | None = field(default=None, kw_only=True)

    @classmethod
    def create(
        cls,
        subscription: Subscription,
        user_id: int, server_id: UUID, discount: Discount | None=None
    ) -> "Order":

        total_price = subscription.price

        if discount:
            total_price = discount.apply(price=total_price)

        order = cls(
            subscription=subscription,
            user_id=user_id,
            server_id=server_id,
            total_price=total_price,
            discount=discount
        )

        return order

    def paid(self) -> None:
        self.payment_date = datetime.now()

        self.register_event(
            PaidOrderEvent(
                order_id=self.id,
                user_id=self.user_id,
                server_id=self.server_id,
                end_time=self.payment_date + self.subscription.duration
            )
        )