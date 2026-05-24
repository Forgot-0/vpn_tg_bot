from __future__ import annotations

from decimal import Decimal

from app.domain.values.money import Money
from app.domain.values.subscriptions import PricingRules, SubscriptionSpec


class PricingService:

    def calculate(self, spec: SubscriptionSpec, rules: PricingRules) -> Money:
        currency = rules.currency
        total = rules.base_fee

        if spec.duration_days is not None:
            total += rules.per_day_rate * spec.duration_days

        if spec.traffic_limit_gb is not None:
            total += rules.per_gb_rate * spec.traffic_limit_gb

        extra_devices = max(0, spec.max_devices - 1)
        total += rules.per_extra_device_rate * extra_devices

        for protocol in spec.protocols:
            rate = rules.per_protocol_rates.get(protocol, Decimal("0"))
            total += rate

        for feature in spec.features:
            rate = rules.per_feature_rates.get(feature, Decimal("0"))
            total += rate

        price = Money(total, currency)

        if rules.minimum_price is not None:
            minimum = Money(rules.minimum_price, currency)
            if price < minimum:
                return minimum

        return price
