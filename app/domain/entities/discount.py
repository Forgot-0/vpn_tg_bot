from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from domain.entities.base import AggregateRoot
from domain.entities.subscription import Subscription


@dataclass
class Discount(AggregateRoot):
    id: UUID
    name: str
    description: str
    percent: float

    subscription_ids: list[UUID] | None = field(default_factory=list)
    end_time: datetime | None = field(default=None)
    max_per_user: int = field(default=0)
    max_uses: int | None = field(default=None)

    uses: int = field(default=0)
    is_active: bool = field(default=True)

    def apply(self, price: float) -> float:
        return (1-self.percent)*price


@dataclass
class DiscountUser(AggregateRoot):
    discount_id: UUID
    user_id: int
    count: int

"""
user_id = 1
list_subs = []
list_discount = []
user_uses = {}

for discount in list_discount:
    if discount.max_per_user:
        if user_uses[user_id] > discount.max_per_user:
            continue

    if max_uses < uses:
        continue

    if discount.subs_id:
        subs = list_subs.get(id)
        discount.apply(subs)
    else:
        for subs in list_subs:
            discount.apply(subs)

"""