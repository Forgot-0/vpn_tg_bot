from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


from domain.entities.base import AggregateRoot
from domain.services.servers import encrypt
from domain.values.servers import api_type_to_model, ApiType, ProtocolConfig, ProtocolType, Region


@dataclass
class Server(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    limit: int
    region: Region
    free: int

    api_type: ApiType
    api_config: dict[str, Any]
    auth_credits: dict[str, str]

    protocol_configs: dict[ProtocolType, ProtocolConfig] = field(default_factory=dict)

    def __post_init__(self):
        api_config_model = api_type_to_model.get(self.api_type)

        if not api_config_model:
            raise

        api_config_model(**self.api_config)

    @classmethod
    def create(cls, limit: int, region: Region, api_type: ApiType, \
            api_config: dict[str, Any], auth_credits: dict[str, str], \
            protocol_configs: dict[ProtocolType, ProtocolConfig] | None = None) -> "Server":

        for key, val in auth_credits.items():
            auth_credits[key] = encrypt(val)

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