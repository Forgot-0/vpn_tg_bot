from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


from domain.entities.base import AggregateRoot
from domain.values.servers import APIConfig, APICredits, ApiType, ProtocolConfig, ProtocolType, Region


@dataclass
class Server(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    limit: int
    region: Region
    free: int

    api_type: ApiType
    api_config: APIConfig
    auth_credits: APICredits

    protocol_configs: dict[ProtocolType, ProtocolConfig] = field(default_factory=dict)


    @classmethod
    def create(cls, limit: int, region: Region, api_type: ApiType, \
            api_config: APIConfig, auth_credits: APICredits, \
            protocol_configs: dict[ProtocolType, ProtocolConfig] | None = None) -> "Server":

        server =  Server(
            limit=limit,
            region=region,
            free=limit,
            api_type=api_type,
            api_config=api_config,
            auth_credits=auth_credits,
            protocol_configs=protocol_configs if protocol_configs else dict()
        )

        return server

    def get_config_by_protocol(self, protocol_type: ProtocolType) -> ProtocolConfig:
        config = self.protocol_configs.get(protocol_type)
        if config is None:
            raise
        return config

    def add_protocol_config(self, config: ProtocolConfig) -> None:
        if config.protocol_type in self.protocol_configs:
            raise
        self.protocol_configs[config.protocol_type] = config