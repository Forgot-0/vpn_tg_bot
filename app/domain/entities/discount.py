from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot


@dataclass
class Discount(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    name: str
    description: str
    percent: float

    subscription_ids: list[UUID] | None = field(default_factory=list)
    end_time: datetime | None = field(default=None)
    max_per_user: int = field(default=0)
    max_uses: int | None = field(default=None)

    uses: int = field(default=0)
    is_active: bool = field(default=True)

    def apply(self, price: float) -> int:
        return int((1-self.percent/100)*price)

    def is_valid(self) -> bool:
        flag = True
        if self.end_time:
            flag = flag and self.end_time > datetime.now()

        if self.max_uses:
            flag = flag and self.max_uses > self.uses

        return flag


@dataclass
class DiscountUser(AggregateRoot):
    discount_id: UUID
    user_id: int
    count: int
