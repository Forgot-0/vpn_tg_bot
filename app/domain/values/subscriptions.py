from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import FrozenSet

from app.domain.values.servers import FeatureCode, ProtocolCode


class ProductType(StrEnum):
    VPN_SUBSCRIPTION = "vpn_subscription"
    DEDICATED_IP = "dedicated_ip"
    EXTRA_TRAFFIC = "extra_traffic"
    EXTRA_DEVICES = "extra_devices"
    TRIAL = "trial"
    BUSINESS = "business"


class PlanType(StrEnum):
    FIXED = "fixed"
    FLEXIBLE = "flexible"


class PlanVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    HIDDEN = "hidden"


class PriceType(StrEnum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    USAGE_BASED = "usage_based"


class BillingInterval(StrEnum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    LIFETIME = "lifetime"


class OfferStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class CheckoutStatus(StrEnum):
    OPEN = "open"
    DRAFT = "draft"
    READY_FOR_PAYMENT = "ready_for_payment"
    READY_FOR_CHECKOUT = "ready_for_checkout"
    COMPLETED = "completed"
    CONVERTED = "converted"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class OrderStatus(StrEnum):
    DRAFT = "draft"
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    FULFILLING = "fulfilling"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class SubscriptionStatus(StrEnum):
    PENDING_PAYMENT = "pending_payment"
    PENDING_PROVISIONING = "pending_provisioning"
    PROVISIONING_FAILED = "provisioning_failed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class AccessFormat(StrEnum):
    SUBSCRIPTION_URL = "subscription_url"
    CONFIG_FILE = "config_file"
    CONNECTION_STRING = "connection_string"


class ProvisioningStatus(StrEnum):
    PENDING = "pending"
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    FAILED = "failed"
    SUSPENDED = "suspended"
    DELETING = "deleting"
    DELETED = "deleted"


class RemoteAccessState(StrEnum):
    UNKNOWN = "unknown"
    EXISTS = "exists"
    MISSING = "missing"
    DISABLED = "disabled"
    DELETED = "deleted"


@dataclass(frozen=True)
class PlanConfiguration:
    protocols: FrozenSet[ProtocolCode]
    duration_days: int | None
    traffic_limit_gb: Decimal | None
    max_devices: int
    features: FrozenSet[FeatureCode] = frozenset()
    location_ids: FrozenSet[str] = frozenset()
    server_group_ids: FrozenSet[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.protocols:
            raise ValueError("At least one protocol is required")
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
class PlanOptionSet:
    allowed_protocols: FrozenSet[ProtocolCode]
    allowed_features: FrozenSet[FeatureCode] = frozenset()
    allowed_location_ids: FrozenSet[str] = frozenset()
    allowed_server_group_ids: FrozenSet[str] = frozenset()

    min_duration_days: int = 1
    max_duration_days: int | None = None
    duration_options_days: FrozenSet[int] = frozenset()

    min_traffic_gb: Decimal | None = None
    max_traffic_gb: Decimal | None = None
    traffic_options_gb: FrozenSet[Decimal] = frozenset()

    min_devices: int = 1
    max_devices: int = 1
    device_options: FrozenSet[int] = frozenset()

    duration_required: bool = True
    traffic_required: bool = False

    def check(self, config: PlanConfiguration) -> list[str]:
        violations: list[str] = []

        disallowed_protocols = config.protocols - self.allowed_protocols
        if disallowed_protocols:
            violations.append(f"Protocols not allowed by plan: {', '.join(disallowed_protocols)}")

        disallowed_features = config.features - self.allowed_features
        if disallowed_features:
            violations.append(f"Features not allowed by plan: {', '.join(disallowed_features)}")

        if self.allowed_location_ids and not config.location_ids.issubset(self.allowed_location_ids):
            violations.append("Locations are not allowed by plan")

        if self.allowed_server_group_ids and not config.server_group_ids.issubset(self.allowed_server_group_ids):
            violations.append("Server groups are not allowed by plan")

        if self.duration_required and config.duration_days is None:
            violations.append("Duration is required for this plan")

        if config.duration_days is not None:
            if config.duration_days < self.min_duration_days:
                violations.append(f"Duration must be >= {self.min_duration_days} days")
            if self.max_duration_days and config.duration_days > self.max_duration_days:
                violations.append(f"Duration must be <= {self.max_duration_days} days")
            if self.duration_options_days and config.duration_days not in self.duration_options_days:
                violations.append("Duration is not available for this plan")

        if self.traffic_required and config.traffic_limit_gb is None:
            violations.append("Traffic limit is required for this plan")

        if config.traffic_limit_gb is not None:
            if self.min_traffic_gb and config.traffic_limit_gb < self.min_traffic_gb:
                violations.append(f"Traffic must be >= {self.min_traffic_gb} GB")
            if self.max_traffic_gb and config.traffic_limit_gb > self.max_traffic_gb:
                violations.append(f"Traffic must be <= {self.max_traffic_gb} GB")
            if self.traffic_options_gb and config.traffic_limit_gb not in self.traffic_options_gb:
                violations.append("Traffic limit is not available for this plan")

        if config.max_devices < self.min_devices:
            violations.append(f"Devices must be >= {self.min_devices}")
        if config.max_devices > self.max_devices:
            violations.append(f"Devices must be <= {self.max_devices}")
        if self.device_options and config.max_devices not in self.device_options:
            violations.append("Device count is not available for this plan")

        return violations


@dataclass(frozen=True)
class PriceContext:
    country_code: str | None = None
    tax_category: str | None = None
    promo_eligible: bool = True
    active_from: date | None = None
    active_to: date | None = None

    def is_active_on(self, value: date) -> bool:
        if self.active_from is not None and value < self.active_from:
            return False
        if self.active_to is not None and value > self.active_to:
            return False
        return True


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


@dataclass(frozen=True)
class SubscriptionLimits:
    duration_days: int | None
    traffic_limit_gb: Decimal | None
    max_devices: int
