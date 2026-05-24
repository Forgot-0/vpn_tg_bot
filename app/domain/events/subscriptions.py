from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.domain.entities.base import DomainEvent


@dataclass(frozen=True)
class SubscriptionActivatedEvent(DomainEvent):
    __event_name__ = "subscription.activated"

    subscription_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    started_at: date
    expires_at: date | None


@dataclass(frozen=True)
class SubscriptionRenewedEvent(DomainEvent):
    __event_name__ = "subscription.renewed"

    subscription_id: UUID
    user_id: UUID
    previous_expires_at: date | None
    new_expires_at: date | None


@dataclass(frozen=True)
class SubscriptionExpiredEvent(DomainEvent):
    __event_name__ = "subscription.expired"

    subscription_id: UUID
    user_id: UUID


@dataclass(frozen=True)
class SubscriptionCancelledEvent(DomainEvent):
    __event_name__ = "subscription.cancelled"

    subscription_id: UUID
    user_id: UUID


@dataclass(frozen=True)
class SubscriptionSuspendedEvent(DomainEvent):
    __event_name__ = "subscription.suspended"

    subscription_id: UUID
    user_id: UUID
    reason: str


@dataclass(frozen=True)
class TrafficConsumedEvent(DomainEvent):
    __event_name__ = "subscription.traffic_consumed"

    subscription_id: UUID
    user_id: UUID
    consumed_gb: Decimal
    total_used_gb: Decimal
