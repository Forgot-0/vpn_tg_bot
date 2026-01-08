from pydantic import BaseModel

from app.domain.entities.price import PriceConfig


class PriceConfigResponse(BaseModel):
    daily_rate: float
    device_rate_multiplier: float
    region_base_multiplier: float
    region_multipliers: dict[str, float]
    protocol_base_multiplier: float
    protocol_multipliers: dict[str, float]

    @classmethod
    def from_price_config(cls, config: PriceConfig) -> 'PriceConfigResponse':
        return PriceConfigResponse(
            daily_rate=config.daily_rate,
            device_rate_multiplier=config.device_rate_multiplier,
            region_base_multiplier=config.region_base_multiplier,
            region_multipliers={
                region.code: config.region_multipliers[region]
                for region in config.region_multipliers
            },
            protocol_base_multiplier=config.protocol_base_multiplier,
            protocol_multipliers={
                protocol.value: config.protocol_multipliers[protocol]
                for protocol in config.protocol_multipliers
            },
        )

