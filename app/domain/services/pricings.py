from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import FrozenSet

from app.domain.entities.subscription_plan import SubscriptionPlan
from app.domain.errors import BusinessRuleViolationError
from app.domain.values.servers import ProtocolCode
from app.domain.values.subscriptions import DeviceCount, Money, PlanFeature


@dataclass(frozen=True)
class RuleBasedPricingService:
    base_fee: Money = Money(Decimal("0"))
    day_rate: Money = Money(Decimal("0"))
    gb_rate: Money = Money(Decimal("0"))
    device_rate: Money = Money(Decimal("0"))
    protocol_rate: dict[ProtocolCode, Money] = field(default_factory=dict)
    feature_rate: dict[str, Money] = field(default_factory=dict)
    traffic_only_flat_fee: Money = Money(Decimal("0"))
    minimum_price: Money | None = None

    def calculate(
        self,
        plan: SubscriptionPlan,
        protocols: FrozenSet[ProtocolCode],
        devices: DeviceCount,
        features: FrozenSet[PlanFeature],
    ) -> Money:
        if not protocols.issubset(plan.allowed_protocols):
            raise BusinessRuleViolationError(reason="selected protocols are not allowed by plan")

        if plan.max_devices is not None and devices > plan.max_devices:
            raise BusinessRuleViolationError(reason="selected device count exceeds plan limit")

        price = self.base_fee

        if plan.duration is not None:
            price += self.day_rate * plan.duration.as_generic_type()

        if plan.traffic_quota is not None:
            price += self.gb_rate * plan.traffic_quota.as_generic_type()

        if plan.duration is None:
            price += self.traffic_only_flat_fee

        extra_devices = max(0, devices.as_generic_type() - 1)
        price += self.device_rate * extra_devices

        for protocol in protocols:
            price += self.protocol_rate.get(protocol, Money(Decimal("0"), price.currency))

        for feature in features:
            key = feature.code.value
            price += self.feature_rate.get(key, Money(Decimal("0"), price.currency)) * feature.quantity

        if self.minimum_price is not None and price.amount < self.minimum_price.amount:
            return self.minimum_price

        return price
