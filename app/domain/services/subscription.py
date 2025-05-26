from dataclasses import dataclass
from domain.entities.subscription import Subscription
from domain.values.servers import ProtocolType, Region


@dataclass
class SubscriptionPricingService:

    daily_rate: float
    device_rate_multiplier: float
    region_multipliers: dict[Region, float]
    protocol_multipliers: dict[ProtocolType, float]

    def calculate(self, subscription: Subscription) -> float:
        if not subscription.is_active():
            return 0
        base_cost = self.daily_rate * subscription.duration

        devices_cost = base_cost * subscription.device_count * self.device_rate_multiplier

        region_coef = self.region_multipliers.get(subscription.region, 1.0)
        region_cost = base_cost * (region_coef - 1)

        protocols_cost = sum(
            base_cost * self.protocol_multipliers.get(protocol, 0)
            for protocol in subscription.protocol_types
        )

        total = base_cost + devices_cost + region_cost + protocols_cost
        return round(total, 2)
