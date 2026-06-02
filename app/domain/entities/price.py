from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.money import Money
from app.domain.values.subscriptions import BillingInterval, PriceContext, PriceType


@dataclass
class Price(AggregateRoot):
    id: UUID
    plan_id: UUID
    money: Money
    price_type: PriceType = PriceType.ONE_TIME
    billing_interval: BillingInterval = BillingInterval.MONTH
    duration_days: int | None = None
    traffic_limit_gb: Decimal | None = None
    device_count: int | None = None
    context: PriceContext = field(default_factory=PriceContext)
    is_active: bool = True
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if self.money.amount <= 0:
            raise ValueError("Price amount must be positive")
        if self.duration_days is not None and self.duration_days < 1:
            raise ValueError("Price duration_days must be >= 1")
        if self.traffic_limit_gb is not None and self.traffic_limit_gb <= 0:
            raise ValueError("Price traffic_limit_gb must be positive")
        if self.device_count is not None and self.device_count < 1:
            raise ValueError("Price device_count must be >= 1")

    def is_available_on(self, value: date) -> bool:
        return self.is_active and self.context.is_active_on(value)
