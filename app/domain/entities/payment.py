from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.entities.discount import Discount
from app.domain.entities.subscription import Subscription
from app.domain.events.paymens.paid import PaidPaymentEvent
from app.domain.services.utils import now_utc
from app.domain.values.users import UserId



class PaymentStatus(Enum):
    pending = "PENDING"
    succese = "SUCCESE"


@dataclass
class Payment(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    subscription: Subscription
    user_id: UserId

    total_price: float

    status: PaymentStatus

    payment_date: datetime | None = field(default=None, kw_only=True)
    payment_id: UUID | None = field(default=None, kw_only=True)
    created_at: datetime = field(
        default_factory=now_utc,
        kw_only=True
    )

    discount: Discount | None = field(default=None, kw_only=True)

    @classmethod
    def create(
        cls,
        subscription: Subscription,
        user_id: UserId,
        price: float,
        discount: Discount | None=None
    ) -> "Payment":

        total_price = price

        if discount:
            total_price = discount.apply(price=total_price)

        order = cls(
            subscription=subscription,
            user_id=user_id,
            total_price=total_price,
            discount=discount,
            status=PaymentStatus.pending
        )

        return order

    def paid(self) -> None:
        self.payment_date = now_utc()
        self.status = PaymentStatus.succese

        self.register_event(
            PaidPaymentEvent(
                order_id=self.id,
                subscription_id=self.subscription.id.value,
                user_id=self.user_id.value,
                end_time=self.payment_date + timedelta(days=self.subscription.duration)
            )
        )