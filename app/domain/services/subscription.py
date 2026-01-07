from dataclasses import dataclass

from app.domain.entities.subscription import Subscription
from app.domain.repositories.price import BasePriceRepository



@dataclass
class SubscriptionPricingService:
    price_repository: BasePriceRepository

    async def calculate(self, subscription: Subscription) -> float:
        cfg = await self.price_repository.get_price_config()

        base_cost = cfg.daily_rate * subscription.duration

        devices_cost = base_cost * subscription.device_count * cfg.device_rate_multiplier

        region_coef = cfg.region_multipliers.get(subscription.region, cfg.region_base_multiplier)
        region_cost = base_cost * (region_coef - 1)

        protocols_cost = sum(
            base_cost * cfg.protocol_multipliers.get(protocol, cfg.protocol_base_multiplier)
            for protocol in subscription.protocol_types
        )

        total = base_cost + devices_cost + region_cost + protocols_cost
        return round(total, 2)

    def change_region(self, subscription: Subscription) -> float:
        return 100.0
