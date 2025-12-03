from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.values.users import UserId


@dataclass
class Discount(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    name: str
    description: str
    percent: float

    conditions: dict[str, Any]

    uses: int = field(default=0)
    is_active: bool = field(default=True)

    def apply(self, price: float) -> int:
        return int((1-self.percent/100)*price)

    def is_valid(self) -> bool:
        flag = True
        if self.conditions.get('end_time'):
            flag = flag and self.conditions['end_time'] > datetime.now()

        if self.conditions.get('max_uses'):
            flag = flag and self.conditions['max_uses'] > self.uses

        return flag


@dataclass
class DiscountUser(AggregateRoot):
    discount_id: UUID
    user_id: UserId
    count: int
