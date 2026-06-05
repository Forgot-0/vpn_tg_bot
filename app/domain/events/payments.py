from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.base import DomainEvent


@dataclass(frozen=True)
class PaymentIntentCreatedEvent(DomainEvent):
    __event_name__ = "payment.created"

    payment_intent_id: UUID
    checkout_session_id: UUID
    user_id: UUID


@dataclass(frozen=True)
class PaymentSucceededEvent(DomainEvent):
    __event_name__ = "payment.succeeded"

    payment_intent_id: UUID
    checkout_session_id: UUID
    external_id: str
