from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import StrEnum
from typing import Final

from app.domain.values.base import BaseValueObject



class BillingMode(StrEnum):
    PERIOD_ONLY = "period_only"
    PERIOD_WITH_TRAFFIC = "period_with_traffic"
    TRAFFIC_ONLY = "traffic_only"


class SubscriptionStatus(StrEnum):
    DRAFT = "draft"
    PENDING_PAYMENT = "pending_payment"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    RENEWED = "renewed"


class AccessFormat(StrEnum):
    LINK = "link"
    CONFIG = "config"
    JSON = "json"


class PlanFeatureCode(StrEnum):
    MULTI_HOP = "multi_hop"
    DEDICATED_IP = "dedicated_ip"
    EXTRA_PORTS = "extra_ports"
    HIGH_SPEED = "high_speed"
    STATIC_IP = "static_ip"


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        normalized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", normalized)

    def _check_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")

    def __add__(self, other: Money) -> Money:
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: int | Decimal) -> Money:
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"


@dataclass(frozen=True)
class DurationDays(BaseValueObject[int]):
    def validate(self) -> None:
        if self.value <= 0:
            raise ValueError("Duration must be positive")

    def as_generic_type(self) -> int:
        return self.value


@dataclass(frozen=True)
class TrafficQuota(BaseValueObject[int]):
    def validate(self) -> None:
        if self.value <= 0:
            raise ValueError("Traffic quota must be positive")

    def as_generic_type(self) -> int:
        return self.value


@dataclass(frozen=True)
class DeviceCount(BaseValueObject[int]):
    def validate(self) -> None:
        if self.value <= 0:
            raise ValueError("Device count must be positive")

    def as_generic_type(self) -> int:
        return self.value

    def __gt__(self, other: object) -> bool:
        if isinstance(other, BaseValueObject):
            return self.value > other.as_generic_type()
        if isinstance(other, int):
            return self.value > other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, BaseValueObject):
            return self.value <= other.as_generic_type()
        if isinstance(other, int):
            return self.value <= other
        return NotImplemented


@dataclass(frozen=True)
class PlanFeature:
    code: PlanFeatureCode
    quantity: Decimal = Decimal("1")

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Feature quantity must be positive")


@dataclass(frozen=True)
class AccessArtifact:
    format: AccessFormat
    value: str
    external_id: str | None = None

    def is_link(self) -> bool:
        return self.format == AccessFormat.LINK
