from dataclasses import dataclass, field
from datetime import timedelta
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.entities.discount import Discount



@dataclass
class Subscription(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    name: str
    description: str
    limit_ip: int = field(default=1, kw_only=True)
    limit_trafic: int = field(default=0, kw_only=True)
    duration: timedelta = field(default_factory=timedelta, kw_only=True)
    price: float
    is_active: bool = field(default=True, kw_only=True)

    discount: Discount | None = field(default=None, kw_only=True)
    price_with_discount: float | None = field(default=None, kw_only=True)

    def set_discount(self, discount: Discount) -> None:
        if self.discount:
            if self.discount.percent > discount.percent:
                return

        self.discount = discount
        self.price_with_discount = self.discount.apply(price=self.price)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, value: UUID) -> bool:
        return self.id == value