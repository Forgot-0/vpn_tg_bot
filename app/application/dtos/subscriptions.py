from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.domain.values.subscriptions import SubscriptionStatus



@dataclass(frozen=True)
class PlanPriceDTO:
    amount: Decimal
    currency: str


@dataclass(frozen=True)
class PlanDTO:
    id: UUID
    code: str
    name: str
    description: str
    prices: list[PlanPriceDTO]

    duration_days: int | None
    traffic_gb: float | None
    max_devices: int | None

    is_trial: bool
    order_index: int


@dataclass(frozen=True)
class SubscriptionDTO:
    id: UUID
    user_id: UUID
    plan_id: UUID
    plan_name: str

    status: SubscriptionStatus

    activated_at: datetime | None
    expires_at: datetime | None

    bytes_used: int
    traffic_limit_bytes: int | None

    duration_days: int | None
    max_devices: int | None


@dataclass(frozen=True)
class CreateSubscriptionResult:
    subscription_id: UUID
    order_id: UUID
    payment_id: UUID
    confirmation_url: str


@dataclass(frozen=True)
class RenewSubscriptionResult:
    subscription_id: UUID
    order_id: UUID
    payment_id: UUID
    confirmation_url: str
