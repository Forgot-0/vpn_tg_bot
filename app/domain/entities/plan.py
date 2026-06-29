from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.errors import PlanNotActiveError
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import (
    DeviceLimit,
    Duration,
    PlanVisibility,
    SubscriptionLimits,
    TrafficLimit,
)


@dataclass
class PricingRule:
    price_per_day: Money
    price_per_gb: Money
    price_per_device: Money
    feature_surcharges: dict[FeatureCode, Money] = field(default_factory=dict)
    protocol_surcharges: dict[ProtocolCode, Money] = field(default_factory=dict)

    def calculate(
        self,
        *,
        duration: Duration,
        traffic: TrafficLimit,
        devices: DeviceLimit,
        features: set[FeatureCode],
        protocols: set[ProtocolCode],
    ) -> Money:
        base = Money.zero(self.price_per_day.currency)

        if duration.days is not None:
            base = base + self.price_per_day * duration.days

        if not traffic.is_unlimited and traffic.gb is not None:
            base = base + self.price_per_gb * traffic.gb

        if devices.max_devices is not None:
            base = base + self.price_per_device * devices.max_devices

        for feature in features:
            surcharge = self.feature_surcharges.get(feature)
            if surcharge:
                base = base + surcharge

        for protocol in protocols:
            surcharge = self.protocol_surcharges.get(protocol)
            if surcharge:
                base = base + surcharge

        return base


@dataclass
class SubscriptionPlan(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)

    code: str
    name: str
    description: str

    limit: SubscriptionLimits | None = field(default=None)

    price: set[Money] = field(default_factory=set)

    price_rule: PricingRule | None = field(default=None)

    visibility: PlanVisibility = field(default=PlanVisibility.PUBLIC)
    order_index: int = field(default=0)
    is_trial: bool = field(default=False)
    is_active: bool = field(default=True)

    allowed_durations: list[int] = field(default_factory=list)
    allowed_traffic_gb: list[float] = field(default_factory=list)
    max_devices_limit: int | None = field(default=None)
    allowed_features: set[FeatureCode] = field(default_factory=set)
    allowed_protocols: set[ProtocolCode] = field(default_factory=set)

    def validate(self) -> None:
        pass

    @property
    def is_fixed(self) -> bool:
        return self.limit is not None

    @property
    def is_dynamic(self) -> bool:
        return self.limit is None and self.price_rule is not None

    def ensure_active(self) -> None:
        if not self.is_active:
            raise PlanNotActiveError()

    def calculate_price(self, limit: SubscriptionLimits) -> Money:
        if self.price_rule is None:
            raise 

        return self.price_rule.calculate(
            duration=limit.duration_days,
            traffic=limit.traffic_limit_gb,
            devices=limit.max_devices,
            features=limit.features,
            protocols=limit.protocols,
        )

    def fixed_price_for(self, currency: str) -> Money | None:
        for p in self.price:
            if p.currency == currency:
                return p
        return None

    @classmethod
    def create_fixed(
        cls,
        *,
        code: str,
        name: str,
        description: str,
        limit: SubscriptionLimits,
        prices: list[Money],
        visibility: PlanVisibility = PlanVisibility.PUBLIC,
        is_trial: bool = False,
    ) -> Self:
        return cls(
            code=code,
            name=name,
            description=description,
            limit=limit,
            price=set(prices),
            visibility=visibility,
            is_trial=is_trial,
        )

    @classmethod
    def create_dynamic(
        cls,
        *,
        code: str,
        name: str,
        description: str,
        price_rule: PricingRule,
        allowed_durations: list[int],
        allowed_traffic_gb: list[float],
        allowed_features: set[FeatureCode],
        allowed_protocols: set[ProtocolCode],
        max_devices_limit: int | None = None,
    ) -> Self:
        return cls(
            code=code,
            name=name,
            description=description,
            price_rule=price_rule,
            allowed_durations=allowed_durations,
            allowed_traffic_gb=allowed_traffic_gb,
            allowed_features=allowed_features,
            allowed_protocols=allowed_protocols,
            max_devices_limit=max_devices_limit,
        )
