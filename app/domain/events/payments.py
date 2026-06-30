from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import DomainEvent


@dataclass(frozen=True)
class PaymentCreatedEvent(DomainEvent):
    __event_name__ = "payment.created"

    payment_id: UUID
    order_id: UUID
    confirmation_url: str


@dataclass(frozen=True)
class PaymentSucceededEvent(DomainEvent):
    __event_name__ = "payment.succeeded"

    payment_id: UUID
    order_id: UUID
    paid_at: datetime


@dataclass(frozen=True)
class PaymentFailedEvent(DomainEvent):
    __event_name__ = "payment.failed"

    payment_id: UUID
    order_id: UUID


@dataclass(frozen=True)
class PaymentCancelledEvent(DomainEvent):
    __event_name__ = "payment.cancelled"

    payment_id: UUID
    order_id: UUID
