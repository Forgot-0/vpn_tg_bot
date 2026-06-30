from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.services.clock import now_utc
from app.domain.values.money import Money
from app.domain.values.order import OrderStatus, OrderType
from app.domain.values.subscriptions import RenewalMode, SubscriptionLimits



@dataclass
class Order(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)

    user_id: UUID
    subscription_id: UUID
    amount: Money

    type: OrderType
    status: OrderStatus

    subscription_limit: SubscriptionLimits | None = field(default=None)
    renewal_mode: RenewalMode | None = field(default=None)
    created_at: datetime = field(default_factory=now_utc)
    paid_at: datetime | None = field(default=None)
    expires_at: datetime | None = field(default=None)

    def validate(self) -> None:
        if self.type == OrderType.RENEW_SUBSCRIPTION and self.renewal_mode is None:
            raise
