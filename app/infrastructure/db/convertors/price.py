from typing import Any

from app.domain.entities.price import PriceConfig
from app.domain.values.servers import ProtocolType, Region


def convert_price_entity_to_document(cfg: PriceConfig) -> dict[str, Any]:
    return {
        "_id": 1,
        "daily_rate": cfg.daily_rate,
        "device_rate_multiplier": cfg.device_rate_multiplier,
        "region_base_multiplier": cfg.region_base_multiplier,
        "region_multipliers": {
            reg_multi.code: cfg.region_multipliers[reg_multi]
            for reg_multi in cfg.region_multipliers
        },
        "protocol_base_multiplier": cfg.protocol_base_multiplier,
        "protocol_multipliers": {
            pro_multi.value: cfg.protocol_multipliers[pro_multi]
            for pro_multi in cfg.protocol_multipliers
        }
    }

def convert_price_document_to_entity(data: dict[str, Any]) -> PriceConfig:
    return PriceConfig(
        daily_rate=data['daily_rate'],
        device_rate_multiplier=data['device_rate_multiplier'],
        region_base_multiplier=data['region_base_multiplier'],
        region_multipliers={
            Region.region_by_code(d): data["region_multipliers"][d]
            for d in data["region_multipliers"]
        },
        protocol_base_multiplier=data['protocol_base_multiplier'],
        protocol_multipliers={
            ProtocolType(d): data["protocol_multipliers"][d]
            for d in data["protocol_multipliers"]
        }
    )
