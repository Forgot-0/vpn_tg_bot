from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import InvalidStateTransitionError
from app.domain.values.payments import PaymentProvider, PaymentStatus
from app.domain.values.subscriptions import Money

@dataclass
class PaymentOrder(AggregateRoot):
    id: UUID
    subscription_id: UUID
    price: Money
    provider: PaymentProvider

    status: PaymentStatus = PaymentStatus.PENDING
    external_payment_id: str | None = None
    confirmation_url: str | None = None
    created_at: datetime | None = None
    paid_at: datetime | None = None

    def validate(self) -> None:
        if not self.id:
            raise ValueError("PaymentOrder id cannot be empty")
        if not self.subscription_id:
            raise ValueError("PaymentOrder must belong to a subscription")
        if self.price.amount <= 0:
            raise ValueError("Payment price must be positive")

    def _ensure_mutable(self) -> None:
        if self.status not in (PaymentStatus.PENDING, PaymentStatus.WAITING_FOR_CAPTURE):
            raise InvalidStateTransitionError(
                reason=f"payment status is {self.status}"
            )

    def set_waiting_for_capture(self, confirmation_url: str) -> None:
        self._ensure_mutable()
        self.status = PaymentStatus.WAITING_FOR_CAPTURE
        self.confirmation_url = confirmation_url

    def confirm(self, external_id: str, paid_at: datetime) -> None:
        self._ensure_mutable()
        self.status = PaymentStatus.SUCCEEDED
        self.external_payment_id = external_id
        self.paid_at = paid_at

    def cancel(self) -> None:
        self._ensure_mutable()
        self.status = PaymentStatus.CANCELED

    @property
    def is_paid(self) -> bool:
        return self.status == PaymentStatus.SUCCEEDED

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            PaymentStatus.SUCCEEDED,
            PaymentStatus.CANCELED,
            PaymentStatus.FAILED,
            PaymentStatus.REFUNDED,
        }
