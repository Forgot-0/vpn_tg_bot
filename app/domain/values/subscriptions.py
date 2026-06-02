from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from typing import FrozenSet

from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode


class SubscriptionStatus(StrEnum):
    PENDING_PAYMENT = "pending_payment"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class DraftStatus(StrEnum):
    DRAFT = "draft"
    READY_FOR_CHECKOUT = "ready_for_checkout"
    CONVERTED = "converted"
    EXPIRED = "expired"


class PlanType(StrEnum):
    FIXED = "fixed"
    FLEXIBLE = "flexible"


class AccessFormat(StrEnum):
    SUBSCRIPTION_URL = "subscription_url"
    CONFIG_FILE = "config_file"
    CONNECTION_STRING = "connection_string"


@dataclass(frozen=True)
class SubscriptionSpec:
    protocols: FrozenSet[ProtocolCode]
    duration_days: int | None
    traffic_limit_gb: Decimal | None
    max_devices: int
    features: FrozenSet[FeatureCode] = frozenset()

    def __post_init__(self) -> None:
        if not self.protocols:
            raise ValueError("At least one protocol required")
        if self.max_devices < 1:
            raise ValueError("max_devices must be >= 1")
        if self.duration_days is not None and self.duration_days < 1:
            raise ValueError("duration_days must be >= 1")
        if self.traffic_limit_gb is not None and self.traffic_limit_gb <= 0:
            raise ValueError("traffic_limit_gb must be positive")

    @property
    def is_time_limited(self) -> bool:
        return self.duration_days is not None

    @property
    def is_traffic_limited(self) -> bool:
        return self.traffic_limit_gb is not None


@dataclass(frozen=True)
class PlanConstraints:
    allowed_protocols: FrozenSet[ProtocolCode]
    allowed_features: FrozenSet[FeatureCode] = frozenset()

    min_duration_days: int = 1
    max_duration_days: int | None = None

    min_traffic_gb: Decimal | None = None
    max_traffic_gb: Decimal | None = None

    min_devices: int = 1
    max_devices: int = 1

    duration_required: bool = True
    traffic_required: bool = False

    def check(self, spec: SubscriptionSpec) -> list[str]:
        violations: list[str] = []

        disallowed_protocols = spec.protocols - self.allowed_protocols
        if disallowed_protocols:
            violations.append(f"Protocols not allowed by plan: {', '.join(disallowed_protocols)}")

        disallowed_features = spec.features - self.allowed_features
        if disallowed_features:
            violations.append(f"Features not allowed by plan: {', '.join(disallowed_features)}")

        if self.duration_required and spec.duration_days is None:
            violations.append("Duration is required for this plan")

        if spec.duration_days is not None:
            if spec.duration_days < self.min_duration_days:
                violations.append(f"Duration must be >= {self.min_duration_days} days")
            if self.max_duration_days and spec.duration_days > self.max_duration_days:
                violations.append(f"Duration must be <= {self.max_duration_days} days")

        if self.traffic_required and spec.traffic_limit_gb is None:
            violations.append("Traffic limit is required for this plan")

        if spec.traffic_limit_gb is not None:
            if self.min_traffic_gb and spec.traffic_limit_gb < self.min_traffic_gb:
                violations.append(f"Traffic must be >= {self.min_traffic_gb} GB")
            if self.max_traffic_gb and spec.traffic_limit_gb > self.max_traffic_gb:
                violations.append(f"Traffic must be <= {self.max_traffic_gb} GB")

        if spec.max_devices < self.min_devices:
            violations.append(f"Devices must be >= {self.min_devices}")
        if spec.max_devices > self.max_devices:
            violations.append(f"Devices must be <= {self.max_devices}")

        return violations


@dataclass(frozen=True)
class PricingRules:
    currency: str = "USD"
    base_fee: Decimal = Decimal("0")
    per_day_rate: Decimal = Decimal("0")
    per_gb_rate: Decimal = Decimal("0")
    per_extra_device_rate: Decimal = Decimal("0")
    per_protocol_rates: dict[ProtocolCode, Decimal] = field(default_factory=dict)
    per_feature_rates: dict[FeatureCode, Decimal] = field(default_factory=dict)
    minimum_price: Decimal | None = None


@dataclass(frozen=True)
class AccessCredential:
    format: AccessFormat
    value: str
    protocol: ProtocolCode | None = None
    panel_client_id: str | None = None
    label: str = ""
