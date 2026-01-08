from pydantic import BaseModel

from app.domain.values.servers import ProtocolType


class AddProtocolPriceRequest(BaseModel):
    protocol: ProtocolType
    coef: float


class AddRegionPriceRequest(BaseModel):
    region: str
    coef: float


class UpdatePriceRequest(BaseModel):
    daily_rate: float
    device_rate_multiplier: float
    region_base_multiplier: float
    region_multipliers: dict[str, float]
    protocol_base_multiplier: float
    protocol_multipliers: dict[str, float]
