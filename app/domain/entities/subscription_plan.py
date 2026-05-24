from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import ProtocolCode
from app.domain.values.subscriptions import (
    BillingMode,
    DeviceCount,
    DurationDays,
    Money,
    PlanFeature,
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
    is_active: bool = True

    def validate(self) -> None:
        if not self.code:
            raise ValueError("Plan code cannot be empty")
        if not self.name:
            raise ValueError("Plan name cannot be empty")
        if not self.allowed_protocols:
            raise ValueError("Plan must allow at least one protocol")
        if self.duration is None and self.traffic_quota is None:
            raise ValueError("Plan must define duration or traffic quota")
        if self.max_devices is not None and self.max_devices.value <= 0:
            raise ValueError("max_devices must be positive")
