from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.events.subscriptions import SubscriptionActivatedEvent, TrafficConsumedEvent
from app.domain.values.servers import ProtocolCode
from app.domain.values.subscriptions import (
    AccessArtifact,
    BillingMode,
    DeviceCount,
    DurationDays,
    Money,
    PlanFeature,
    SubscriptionStatus,
    TrafficQuota,
)


@dataclass
class SubscriptionPlan(AggregateRoot):
    id: UUID
    code: str
    name: str
    billing_mode: BillingMode

    duration: DurationDays | None = None
    traffic_quota: TrafficQuota | None = None

    allowed_protocols: FrozenSet[ProtocolCode] = frozenset()
    included_features: FrozenSet[PlanFeature] = frozenset()
    max_devices: DeviceCount | None = None

    fixed_price: Money | None = None

    def validate(self) -> None:
        if not self.allowed_protocols:
            raise ValueError("plan must allow at least one protocol")
        if self.duration is None and self.traffic_quota is None:
            raise ValueError("plan must define duration or traffic quota")
        if self.max_devices is not None and self.max_devices <= 0:
            raise ValueError("max_devices must be positive")


@dataclass(frozen=True)
class SubscriptionRenewal:
    id: UUID
    subscription_id: UUID
    renewed_at: datetime

    previous_expires_at: date | None
    new_expires_at: date | None

    renewal_period_days: int | None
    price_paid: Money
    payment_id: str | None = None
    renewed_by: str | None = None


@dataclass(frozen=True)
class AccessRotation:
    id: UUID
    subscription_id: UUID
    rotated_at: datetime
    reason: str

    old_access_items: list[AccessArtifact]
    new_access_items: list[AccessArtifact]

    rotated_by: str | None = None


@dataclass
class Subscription(AggregateRoot):
    id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    payment_order_id: UUID | None

    protocols: FrozenSet[ProtocolCode]
    devices: DeviceCount
    status: SubscriptionStatus = SubscriptionStatus.PENDING

    started_at: date | None = None
    expires_at: date | None = None

    purchased_price: Money | None = None
    used_traffic_gb: Decimal = Decimal("0")

    access_items: list[AccessArtifact] = field(default_factory=list)
    renewals: list[SubscriptionRenewal] = field(default_factory=list)
    access_rotations: list[AccessRotation] = field(default_factory=list)

    def validate(self) -> None:
        if not self.id:
            raise ValueError("Subscription id cannot be empty")
        if not self.user_id:
            raise ValueError("Subscription must belong to a user")
        if not self.protocols:
            raise ValueError("Subscription must have at least one protocol")

    def activate(self, start_date: date, duration_days: int | None) -> None:
        if self.status not in (SubscriptionStatus.PENDING, SubscriptionStatus.RENEWED):
            raise ValueError(
                f"Cannot activate subscription with status '{self.status}'"
            )

        self.status = SubscriptionStatus.ACTIVE
        self.started_at = start_date
        self.expires_at = (
            None if duration_days is None
            else start_date + timedelta(days=duration_days)
        )

        self.register_event(
            SubscriptionActivatedEvent(
                subscription_id=str(self.id),
                user_id=str(self.user_id),
                plan_id=str(self.plan_id),
                started_at=self.started_at,
                expires_at=self.expires_at,
            )
        )

    def consume_traffic(self, gb: Decimal) -> None:
        if gb <= 0:
            raise ValueError("Traffic must be positive")

        self.used_traffic_gb += gb

        self.register_event(
            TrafficConsumedEvent(
                subscription_id=str(self.id),
                user_id=str(self.user_id),
                consumed_gb=gb,
                total_used_gb=self.used_traffic_gb,
            )
        )

    def mark_pending_payment(self, payment_order_id: UUID) -> None:
        self.status = SubscriptionStatus.PENDING_PAYMENT
        self.payment_order_id = payment_order_id

    def apply_usage(self, gb: Decimal) -> None:
        if gb <= 0:
            raise ValueError("usage must be positive")
        self.used_traffic_gb += gb

    def renew(self, renewal: "SubscriptionRenewal") -> None:
        self.renewals.append(renewal)
        self.expires_at = renewal.new_expires_at
        self.status = SubscriptionStatus.RENEWED

    def rotate_access(self, rotation: "AccessRotation") -> None:
        self.access_rotations.append(rotation)
        self.access_items = rotation.new_access_items
