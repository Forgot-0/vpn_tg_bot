from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.entities.discount import Discount
from domain.entities.subscription import Subscription
from domain.events.orders.paid import PaidOrderEvent
from domain.values.users import UserId



class PaymentStatus(Enum):
    pending = "PENDING"
    succese = "SUCCESE"


@dataclass
class Order(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    subscription: Subscription
    user_id: UserId

    total_price: float

    status: PaymentStatus

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
        user_id: UserId,
        discount: Discount | None=None
    ) -> "Order":

        total_price = subscription.calculate_price()

        if discount:
            total_price = discount.apply(price=total_price)

        order = cls(
            subscription=subscription,
            user_id=user_id,
            total_price=total_price,
            discount=discount,
            status=PaymentStatus("PENDING")
        )

        return order

    def paid(self) -> None:
        self.payment_date = datetime.now()
        self.status = PaymentStatus("SUCCESE")

        self.register_event(
            PaidOrderEvent(
                order_id=self.id,
                user_id=self.user_id,
                end_time=self.payment_date + timedelta(days=self.subscription.duration)
            )
        )