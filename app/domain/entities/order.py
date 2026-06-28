from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.services.clock import now_utc
from app.domain.values.money import Money
from app.domain.values.order import OrderStatus



@dataclass
class Order(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)

    user_id: UUID
    subscription_id: UUID
    amount: Money

    status: OrderStatus
    created_at: datetime = field(default_factory=now_utc)
    paid_at: datetime | None = field(default=None)

    def validate(self) -> None:
        ...
