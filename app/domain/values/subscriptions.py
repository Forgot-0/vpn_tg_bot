
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum
from uuid import UUID

from app.domain.values.base import BaseValueObject
from app.domain.values.servers import PanelType


class BillingMode(StrEnum):
    PERIOD_ONLY = "period_only"
    PERIOD_WITH_TRAFFIC = "period_with_traffic"
    TRAFFIC_ONLY = "traffic_only"


class SubscriptionStatus(StrEnum):
    PENDING = "pending"
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


class SubscriptionId(BaseValueObject[UUID]):
    def validate(self):
        if not self.value:
            raise 

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        normalized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", normalized)

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: int | Decimal) -> "Money":
        factor_decimal = Decimal(str(factor))
        return Money(self.amount * factor_decimal, self.currency)

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise 

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

@dataclass(frozen=True)
class TrafficQuota(BaseValueObject[int]):
    def validate(self):
        if self.value <= 0:
            raise ValueError("Traffic quota must be positive")

    def as_generic_type(self) -> int:
        return self.value


@dataclass(frozen=True)
class DurationDays(BaseValueObject[int]):
    def validate(self):
        if self.value <= 0:
            raise ValueError("Duration must be positive")

    def as_generic_type(self) -> int:
        return self.value

@dataclass(frozen=True)
class DeviceCount(BaseValueObject[int]):
    def validate(self):
        if self.value <= 0:
            raise ValueError("Device count must be positive")

    def as_generic_type(self) -> int:
        return self.value

    def __gt__(self, other: BaseValueObject):
        return self.value > other.as_generic_type()


@dataclass(frozen=True)
class VPNProtocol(BaseValueObject[str]):
    def validate(self):
        normalized = self.value.strip().lower()
        if not normalized:
            raise ValueError("Protocol code cannot be empty")
        object.__setattr__(self, "code", normalized)

    def as_generic_type(self) -> str:
        return self.value



@dataclass(frozen=True)
class ServerSnapshot:
    server_id: str
    panel_type: PanelType
    name: str
    host: str
    region: str | None = None


@dataclass(frozen=True)
class AccessArtifact:
    format: AccessFormat
    value: str
    external_id: str | None = None

    def is_link(self) -> bool:
        return self.format == AccessFormat.LINK



@dataclass(frozen=True)
class PlanFeature:
    code: PlanFeatureCode
    quantity: Decimal = Decimal("1")

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Feature quantity must be positive")

