from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.errors import InvalidStateTransitionError
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

    def mark_paid(self, *, paid_at: datetime) -> None:
        if self.status == OrderStatus.PAID:
            return

        if self.status not in {OrderStatus.CREATED, OrderStatus.WAITING_PAYMENT}:
            raise InvalidStateTransitionError(
                reason=f"Order cannot be paid from status: {self.status.value}"
            )

        self.status = OrderStatus.PAID
        self.paid_at = paid_at

    def mark_failed(self) -> None:
        if self.status in {OrderStatus.PAID, OrderStatus.CANCELLED, OrderStatus.REFUNDED}:
            return

        self.status = OrderStatus.FAILED

    def mark_cancelled(self) -> None:
        if self.status in {OrderStatus.PAID, OrderStatus.CANCELLED, OrderStatus.REFUNDED}:
            return

        self.status = OrderStatus.CANCELLED
