
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.server import Server
from app.domain.values.servers import ProtocolConfig, ProtocolType, SubscriptionConfig




@dataclass
class ServerDTO(BaseDTO):
    id: UUID
    limit: int

    # region
    region_flag: str
    region_code: str
    region_name: str

    free: int
    api_type: str

    # api config
    ip: str
    panel_port: int
    panel_path: str
    domain: str | None

    protocol_configs: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ServerDTO":
        ...

    @classmethod
    def from_entity(cls, entity: Server) -> "ServerDTO":
        return ServerDTO(
            id=entity.id,
            limit=entity.limit,
            region_flag=entity.region.flag,
            region_code=entity.region.code,
            region_name=entity.region.name,
            free=entity.free,
            api_type=entity.api_type.value,
            ip=entity.api_config.ip,
            panel_port=entity.api_config.panel_port,
            panel_path=entity.api_config.panel_path,
            domain=entity.api_config.domain,
            protocol_configs=[protocol.value for protocol in entity.protocol_configs],
        )


@dataclass
class ServerDetailDTO(BaseDTO):
    id: UUID
    limit: int

    # region
    region_flag: str
    region_code: str
    region_name: str

    free: int
    api_type: str

    # api config
    ip: str
    panel_port: int
    panel_path: str
    domain: str | None

    protocol_configs: dict[str, dict[str, Any]]
    subscription_config: SubscriptionConfig | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ServerDetailDTO":
        ...

    @classmethod
    def from_entity(cls, entity: Server) -> "ServerDetailDTO":
        return ServerDetailDTO(
            id=entity.id,
            limit=entity.limit,
            region_flag=entity.region.flag,
            region_code=entity.region.code,
            region_name=entity.region.name,
            free=entity.free,
            api_type=entity.api_type.value,
            ip=entity.api_config.ip,
            panel_port=entity.api_config.panel_port,
            panel_path=entity.api_config.panel_path,
            domain=entity.api_config.domain,
            protocol_configs={
                protocol:entity.protocol_configs[protocol].config 
                for protocol in entity.protocol_configs
            },
            subscription_config=entity.subscription_config
        )
