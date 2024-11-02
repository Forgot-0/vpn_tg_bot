from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID

from domain.entities.base import AggregateRoot
from domain.events.subscriptions.created import NewSubscriptionEvent
from domain.events.subscriptions.paid import PaidSubscriptionEvent


class ProductType(Enum):
    ONE_MONTH = 1
    THREE_MONTH = 3
    SIX_MONTH = 6
    ONE_YEAR = 12


@dataclass
class Subscription(AggregateRoot):
    tg_id: int
    product: ProductType
    server_id: UUID
    limitIp: int = 1
    amount: int = field(default=0, kw_only=True)
    end_time: datetime = field(default_factory=datetime.now())
    is_pay: bool = field(default=False, kw_only=True)
    vpn_url: str | None = field(default=None, kw_only=True)
    payment_id: str | None = field(default=None, kw_only=True)

    @classmethod
    def create(cls, tg_id: int, product: ProductType, server_id: UUID) -> 'Subscription':

        if product.value == 1:
            end_date = datetime.now() + timedelta(product.value*30)
            amount = 100

        elif product.value == 3:
            end_date = datetime.now() + timedelta(days=product.value*30)
            amount = 300

        elif product.value == 6:
            end_date = datetime.now() + timedelta(days=product.value*30)
            amount = 600

        elif product.value == 12:
            end_date = datetime.now() + timedelta(days=product.value*30)
            amount = 1200

        subscription = cls(
            tg_id=tg_id,
            server_id=server_id,
            product=product,
            amount=amount,
            end_time=end_date,
        )

        # subscription.register_event(NewSubscriptionEvent(
        #     subscription_id=subscription.id,
        #     tg_id=subscription.tg_id,
        #     product=subscription.product.value,
        #     amount=subscription.amount,
        #     end_time=end_date,
        # ))

        return subscription

    def paid(self):
        self.register_event(
            PaidSubscriptionEvent(
                subscription_id=self.id,
                tg_id=self.tg_id,
                server_id=self.server_id,
                product=self.product.value,
                amount=self.amount,
                end_time=self.end_time,
            )
        )
