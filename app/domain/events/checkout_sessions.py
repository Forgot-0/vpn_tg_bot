from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import DomainEvent
from app.domain.values.money import Money
from app.domain.values.subscriptions import CheckoutStatus


@dataclass(frozen=True)
class CheckoutSessionCreatedEvent(DomainEvent):
    __event_name__ = "subscription_checkout.created"

    checkout_session_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID | None
    status: CheckoutStatus
    calculated_price: Money | None


@dataclass(frozen=True)
class CheckoutSessionUpdatedEvent(DomainEvent):
    __event_name__ = "subscription_checkout.updated"

    checkout_session_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID | None
    status: CheckoutStatus
    calculated_price: Money | None


@dataclass(frozen=True)
class CheckoutSessionReadyForCheckoutEvent(DomainEvent):
    __event_name__ = "subscription_checkout.ready_for_checkout"

    checkout_session_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    calculated_price: Money


@dataclass(frozen=True)
class CheckoutSessionConvertedEvent(DomainEvent):
    __event_name__ = "subscription_checkout.converted"

    checkout_session_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    payment_intent_id: UUID


@dataclass(frozen=True)
class CheckoutSessionExpiredEvent(DomainEvent):
    __event_name__ = "subscription_checkout.expired"

    checkout_session_id: UUID
    user_id: UUID
    plan_id: UUID

