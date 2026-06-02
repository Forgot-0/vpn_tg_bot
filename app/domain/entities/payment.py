from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import InvalidStateTransitionError
from app.domain.events.payments import PaymentIntentCreatedEvent, PaymentSucceededEvent
from app.domain.values.money import Money
from app.domain.values.payments import PaymentProvider, PaymentStatus


@dataclass
class PaymentIntent(AggregateRoot):
    id: UUID
    user_id: UUID
    amount: Money
    provider: PaymentProvider

    order_id: UUID | None = None
    checkout_session_id: UUID | None = None

    status: PaymentStatus = PaymentStatus.PENDING
    external_id: str | None = None
    confirmation_url: str | None = None
    idempotency_key: str | None = None
    provider_payload: dict[str, object] = field(default_factory=dict)
    created_at: datetime | None = None
    paid_at: datetime | None = None

    def validate(self) -> None:
        if self.amount.amount <= 0:
            raise ValueError("Payment amount must be positive")
        if self.order_id is None and self.checkout_session_id is None:
            raise ValueError("Payment intent must reference order_id or checkout_session_id")

    def awaiting_confirmation(self, *, external_id: str, confirmation_url: str) -> None:
        self._require_mutable()
        self.status = PaymentStatus.WAITING_FOR_CAPTURE
        self.external_id = external_id
        self.confirmation_url = confirmation_url
        self.register_event(
            PaymentIntentCreatedEvent(
                payment_intent_id=self.id,
                checkout_session_id=self.checkout_session_id or self.order_id or self.id,
                user_id=self.user_id,
            )
        )

    def succeed(self, *, external_id: str, paid_at: datetime) -> None:
        self._require_mutable()
        self.status = PaymentStatus.SUCCEEDED
        self.external_id = external_id
        self.paid_at = paid_at
        self.register_event(
            PaymentSucceededEvent(
                payment_intent_id=self.id,
                checkout_session_id=self.checkout_session_id or self.order_id or self.id,
                external_id=external_id,
            )
        )

    def cancel(self) -> None:
        self._require_mutable()
        self.status = PaymentStatus.CANCELLED

    def fail(self) -> None:
        self._require_mutable()
        self.status = PaymentStatus.FAILED

    def refund(self) -> None:
        if self.status != PaymentStatus.SUCCEEDED:
            raise InvalidStateTransitionError(reason="Only succeeded payments can be refunded")
        self.status = PaymentStatus.REFUNDED

    @property
    def is_paid(self) -> bool:
        return self.status == PaymentStatus.SUCCEEDED

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            PaymentStatus.SUCCEEDED,
            PaymentStatus.CANCELLED,
            PaymentStatus.FAILED,
            PaymentStatus.REFUNDED,
        }

    def _require_mutable(self) -> None:
        if self.status not in {PaymentStatus.PENDING, PaymentStatus.WAITING_FOR_CAPTURE}:
            raise InvalidStateTransitionError(
                reason=f"Payment is already in terminal status: {self.status}"
            )
