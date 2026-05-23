from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import FrozenSet

from app.domain.entities.base import AggregateRoot
from app.domain.events.subscriptions import SubscriptionActivatedEvent, TrafficConsumedEvent
from app.domain.values.subscriptions import (
    AccessArtifact,
    BillingMode,
    DeviceCount,
    DurationDays,
    Money,
    PlanFeature,
    SubscriptionStatus,
    TrafficQuota,
    VPNProtocol,
)


@dataclass
class SubscriptionPlan:
    id: str
    code: str
    name: str
    billing_mode: BillingMode

    duration: DurationDays | None = None
    traffic_quota: TrafficQuota | None = None

    allowed_protocols: FrozenSet[VPNProtocol] = frozenset()
    included_features: FrozenSet[PlanFeature] = frozenset()
    max_devices: DeviceCount | None = None

    fixed_price: Money | None = None

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.billing_mode == BillingMode.PERIOD_ONLY:
            if self.duration is None:
                raise ValueError("PERIOD_ONLY requires duration")
            if self.traffic_quota is not None:
                raise ValueError("PERIOD_ONLY must not have traffic quota")

        elif self.billing_mode == BillingMode.PERIOD_WITH_TRAFFIC:
            if self.duration is None or self.traffic_quota is None:
                raise ValueError("PERIOD_WITH_TRAFFIC requires duration and traffic quota")

        elif self.billing_mode == BillingMode.TRAFFIC_ONLY:
            if self.traffic_quota is None:
                raise ValueError("TRAFFIC_ONLY requires traffic quota")
            if self.duration is not None:
                raise ValueError("TRAFFIC_ONLY must not have duration")

        else:
            raise ValueError(f"Unknown billing mode: {self.billing_mode}")


@dataclass(frozen=True)
class SubscriptionRenewal:
    id: str
    subscription_id: str
    renewed_at: datetime

    previous_expires_at: date | None
    new_expires_at: date | None

    renewal_period_days: int | None
    price_paid: Money
    payment_id: str | None = None
    renewed_by: str | None = None


@dataclass(frozen=True)
class AccessRotation:
    id: str
    subscription_id: str
    rotated_at: datetime
    reason: str

    old_access_items: list[AccessArtifact]
    new_access_items: list[AccessArtifact]

    rotated_by: str | None = None


@dataclass
class Subscription(AggregateRoot):
    id: str
    user_id: str
    plan_id: str
    server_id: str

    protocols: FrozenSet[VPNProtocol]
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

        self.used_traffic_gb += gb

        self.register_event(
            TrafficConsumedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                consumed_gb=gb,
                total_used_gb=self.used_traffic_gb,
            )
        )
