from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from app.domain.services.clock import now_utc
from app.domain.values.servers import FeatureCode, ProtocolCode



class PlanVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    HIDDEN = "hidden"


class SubscriptionStatus(StrEnum):
    PENDING_PAYMENT = "pending_payment"
    PENDING_PROVISIONING = "pending_provisioning"
    PROVISIONING_FAILED = "provisioning_failed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"



class TrafficLimitStrategy(StrEnum):
    NO_RESET = "NO_RESET"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    MONTH_ROLLING = "MONTH_ROLLING"


@dataclass
class VpnClient:
    server_id: UUID
    provider_external_id: str


class TrafficResetStrategy(StrEnum):
    NO_RESET = "no_reset"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    EVERY_N_DAYS = "every_n_days"
    CUSTOM = "custom"


@dataclass(frozen=True)
class TrafficLimit:
    bytes_limit: int | None

    @classmethod
    def unlimited(cls) -> TrafficLimit:
        return cls(bytes_limit=None)

    @classmethod
    def from_gb(cls, gb: float) -> TrafficLimit:
        return cls(bytes_limit=int(gb * 1024 ** 3))

    @classmethod
    def from_tb(cls, tb: float) -> TrafficLimit:
        return cls(bytes_limit=int(tb * 1024 ** 4))

    @property
    def is_unlimited(self) -> bool:
        return self.bytes_limit is None

    @property
    def gb(self) -> float | None:
        if self.bytes_limit is None:
            return None

        return self.bytes_limit / 1024 ** 3

    def __add__(self, other: TrafficLimit) -> TrafficLimit:
        if self.is_unlimited or other.is_unlimited:
            return TrafficLimit.unlimited()

        return TrafficLimit(self.bytes_limit + other.bytes_limit)  # type: ignore[operator]


@dataclass(frozen=True)
class Duration:
    days: int | None

    @classmethod
    def lifetime(cls) -> Duration:
        return cls(days=None)

    @classmethod
    def of_days(cls, n: int) -> Duration:
        if n <= 0:
            raise

        return cls(days=n)

    @classmethod
    def of_months(cls, n: int) -> Duration:
        return cls(days=n * 30)

    @property
    def is_lifetime(self) -> bool:
        return self.days is None

    @property
    def as_timedelta(self) -> timedelta | None:
        if self.days is None:
            return None

        return timedelta(days=self.days)

    def __add__(self, other: Duration) -> Duration:
        if self.is_lifetime or other.is_lifetime:
            return Duration.lifetime()

        return Duration(self.days + other.days)  # type: ignore[operator]        


@dataclass(frozen=True)
class DeviceLimit:
    max_devices: int | None = None

    @classmethod
    def unlimited(cls) -> DeviceLimit:
        return cls(max_devices=None)


@dataclass(frozen=True)
class TrafficResetPolicy:
    strategy: TrafficResetStrategy
    reset_every_n_days: int | None = None
    custom_cron: str | None = None

    def __post_init__(self) -> None:
        if self.strategy == TrafficResetStrategy.EVERY_N_DAYS:
            if not self.reset_every_n_days or self.reset_every_n_days <= 0:
                raise 

        if self.strategy == TrafficResetStrategy.CUSTOM:
            if not self.custom_cron:
                raise 

    @classmethod
    def no_reset(cls) -> TrafficResetPolicy:
        return cls(strategy=TrafficResetStrategy.NO_RESET)

    @classmethod
    def monthly(cls) -> TrafficResetPolicy:
        return cls(strategy=TrafficResetStrategy.MONTHLY)


@dataclass(frozen=True)
class SubscriptionLimits:
    duration_days: Duration
    traffic_limit_gb: TrafficLimit
    max_devices: DeviceLimit

    features: set[FeatureCode]
    protocols: set[ProtocolCode]
    traffic_limit_strategy: TrafficResetPolicy


@dataclass
class UsageStats:
    bytes_used: int = 0
    active_devices: int = 0
    last_reset_at: datetime | None = None

    def record_traffic(self, bytes_delta: int) -> None:
        if bytes_delta < 0:
            raise

        self.bytes_used += bytes_delta

    def reset_traffic(self) -> None:
        self.bytes_used = 0
        self.last_reset_at = now_utc()

    @property
    def gb_used(self) -> float:
        return self.bytes_used / 1024 ** 3

