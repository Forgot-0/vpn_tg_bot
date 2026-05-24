from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.base import DomainEvent


@dataclass(frozen=True)
class PaymentOrderCreatedEvent(DomainEvent):
    __event_name__ = "payment.created"

    payment_order_id: UUID
    subscription_id: UUID
    user_id: UUID


@dataclass(frozen=True)
class PaymentSucceededEvent(DomainEvent):
    __event_name__ = "payment.succeeded"

    payment_order_id: UUID
    subscription_id: UUID
    external_id: str
