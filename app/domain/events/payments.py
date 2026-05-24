from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import DomainEvent


@dataclass(frozen=True)
class PaymentOrderCreatedEvent(DomainEvent):
    __event_name__ = "payment_order.created"

    payment_order_id: UUID
    subscription_id: UUID


@dataclass(frozen=True)
class PaymentSucceededEvent(DomainEvent):
    __event_name__ = "payment_order.succeeded"

    payment_order_id: UUID
    subscription_id: UUID
    external_payment_id: str
