from dataclasses import dataclass

from app.domain.values.servers import ProtocolType, Region


@dataclass
class PriceConfig:
    daily_rate: float
    device_rate_multiplier: float
    region_base_multiplier: float
    region_multipliers: dict[Region, float]
    protocol_base_multiplier: float
    protocol_multipliers: dict[ProtocolType, float]
