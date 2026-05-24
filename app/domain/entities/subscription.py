from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta, datetime
from decimal import Decimal
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.events.subscriptions import (
    SubscriptionActivatedEvent,
    SubscriptionRenewedEvent,
    SubscriptionAccessRotatedEvent,
    TrafficConsumedEvent,
)
from app.domain.errors import InvalidStateTransitionError
from app.domain.values.servers import ProtocolCode
from app.domain.values.subscriptions import (
    AccessArtifact,
    Money,
    PlanFeature,
    SubscriptionStatus,
)


@dataclass
class Subscription(AggregateRoot):
    id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    payment_order_id: UUID | None = None

    status: SubscriptionStatus = SubscriptionStatus.DRAFT

    started_at: date | None = None
    expires_at: date | None = None

    purchased_price: Money | None = None
    used_traffic_gb: Decimal = Decimal("0")

    access_items: list[AccessArtifact] = field(default_factory=list)

    allowed_protocols: FrozenSet[ProtocolCode] = frozenset()
    allowed_features: FrozenSet[PlanFeature] = frozenset()

    def validate(self) -> None:
        if not self.id:
            raise ValueError("Subscription id cannot be empty")
        if not self.user_id:
            raise ValueError("Subscription must belong to user")
        if not self.plan_id:
            raise ValueError("Subscription must have plan_id")
        if not self.server_id:
            raise ValueError("Subscription must have server_id")

    def mark_pending_payment(self, payment_order_id: UUID) -> None:
        if self.status not in {SubscriptionStatus.DRAFT, SubscriptionStatus.RENEWED}:
            raise InvalidStateTransitionError(reason=f"subscription status is {self.status}")
        self.payment_order_id = payment_order_id
        self.status = SubscriptionStatus.PENDING_PAYMENT

    def activate(self, start_date: date, duration_days: int | None) -> None:
        if self.status not in {SubscriptionStatus.PENDING_PAYMENT, SubscriptionStatus.RENEWED, SubscriptionStatus.DRAFT}:
            raise InvalidStateTransitionError(reason=f"subscription status is {self.status}")

        self.status = SubscriptionStatus.ACTIVE
        self.started_at = start_date
        self.expires_at = None if duration_days is None else start_date + timedelta(days=duration_days)

        self.register_event(
            SubscriptionActivatedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                started_at=self.started_at,
                expires_at=self.expires_at,
            )
        )

    def consume_traffic(self, gb: Decimal) -> None:
        if gb <= 0:
            raise ValueError("Traffic must be positive")
        if self.status != SubscriptionStatus.ACTIVE:
            raise InvalidStateTransitionError(reason="traffic can be consumed only on active subscription")

        self.used_traffic_gb += gb
        self.register_event(
            TrafficConsumedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                consumed_gb=gb,
                total_used_gb=self.used_traffic_gb,
            )
        )

    def renew(self, new_expires_at: date | None, renewed_at: datetime) -> None:
        if self.status not in {SubscriptionStatus.ACTIVE, SubscriptionStatus.EXPIRED, SubscriptionStatus.RENEWED}:
            raise InvalidStateTransitionError(reason=f"subscription status is {self.status}")

        previous = self.expires_at
        self.expires_at = new_expires_at
        self.status = SubscriptionStatus.RENEWED

        self.register_event(
            SubscriptionRenewedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                previous_expires_at=previous,
                new_expires_at=new_expires_at,
            )
        )

    def rotate_access(self, new_access_items: list[AccessArtifact], reason: str) -> None:
        if self.status not in {SubscriptionStatus.ACTIVE, SubscriptionStatus.RENEWED}:
            raise InvalidStateTransitionError(reason=f"subscription status is {self.status}")

        self.access_items = new_access_items

        self.register_event(
            SubscriptionAccessRotatedEvent(
                subscription_id=self.id,
                reason=reason,
            )
        )

    def expire(self) -> None:
        if self.status not in {SubscriptionStatus.ACTIVE, SubscriptionStatus.RENEWED}:
            raise InvalidStateTransitionError(reason=f"subscription status is {self.status}")
        self.status = SubscriptionStatus.EXPIRED

    def revoke(self) -> None:
        self.status = SubscriptionStatus.REVOKED
