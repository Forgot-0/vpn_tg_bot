from dataclasses import asdict
from typing import Any

from app.domain.entities.server import ProtocolConfig, Server
from app.domain.values.servers import APIConfig, APICredits, ApiType, ProtocolType, Region


def convert_server_entity_to_document(server: Server) -> dict[str, Any]:
    return {
        "_id": server.id,
        "limit": server.limit,
        "region": {
                "flag": server.region.flag,
                "name": server.region.name,
                "code": server.region.code
            },
        "free": server.free,
        "api_type": server.api_type.value,
        "api_config": asdict(server.api_config),
        "auth_credits": asdict(server.auth_credits),
        "protocol_configs": {
            protocol.value: {
                "config": config.config,
                "protocol_type": config.protocol_type.value
            }
            for protocol, config in server.protocol_configs.items()
        }
    }

def convert_server_document_to_entity(data: dict[str, Any]) -> Server:
    return Server(
        id=data['_id'],
        limit=data['limit'],
        region=Region(**data['region']),
        free=data['free'],
        api_type=ApiType(data['api_type']),
        api_config=APIConfig(**data['api_config']),
        auth_credits=APICredits(**data['auth_credits']),
        protocol_configs={
            ProtocolType(key): ProtocolConfig(
                config=value["config"],
                protocol_type=ProtocolType(key)
            )
            for key, value in data.get("protocol_configs", {}).items()
        }
    )
