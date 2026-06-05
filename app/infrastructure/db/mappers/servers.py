from __future__ import annotations

from app.domain.entities.server import CapacityPolicy, VPNServer
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.infrastructure.db.mappers._serialization import (
    dump_enum_set,
    dump_optional_str_set,
    load_enum_set,
)
from app.infrastructure.db.models.servers import VPNServerModel


class VPNServerMapper:
    @staticmethod
    def to_entity(model: VPNServerModel) -> VPNServer:
        return VPNServer(
            id=model.id,
            name=model.name,
            region_code=model.region_code,
            panel_connection_id=model.panel_connection_id,
            location_id=model.location_id,
            server_group_id=model.server_group_id,
            supported_protocols=load_enum_set(model.supported_protocols, ProtocolCode),
            supported_features=load_enum_set(model.supported_features, FeatureCode),
            is_active=model.is_active,
            max_clients=model.max_clients,
            current_clients=model.current_clients,
            capacity_policy=CapacityPolicy(
                max_clients=model.max_clients,
                weight=model.weight,
            ),
            tags=frozenset(model.tags or []),
            panel_config=model.panel_config or {},
        )

    @staticmethod
    def to_model(entity: VPNServer) -> VPNServerModel:
        return VPNServerModel(
            id=entity.id,
            name=entity.name,
            region_code=entity.region_code,
            panel_connection_id=entity.panel_connection_id,
            location_id=entity.location_id,
            server_group_id=entity.server_group_id,
            supported_protocols=dump_enum_set(entity.supported_protocols),
            supported_features=dump_enum_set(entity.supported_features),
            is_active=entity.is_active,
            max_clients=entity.max_clients,
            current_clients=entity.current_clients,
            free=(
                entity.max_clients - entity.current_clients
                if entity.max_clients is not None
                else None
            ),
            weight=entity.capacity_policy.weight,
            tags=dump_optional_str_set(entity.tags),
            panel_config=entity.panel_config,
        )

    @staticmethod
    def update_model(model: VPNServerModel, entity: VPNServer) -> None:
        model.name = entity.name
        model.region_code = entity.region_code
        model.panel_connection_id = entity.panel_connection_id
        model.location_id = entity.location_id
        model.server_group_id = entity.server_group_id
        model.supported_protocols = dump_enum_set(entity.supported_protocols)
        model.supported_features = dump_enum_set(entity.supported_features)
        model.is_active = entity.is_active
        model.max_clients = entity.max_clients
        model.current_clients = entity.current_clients
        model.free = (
            entity.max_clients - entity.current_clients
            if entity.max_clients is not None
            else None
        )
        model.weight = entity.capacity_policy.weight
        model.tags = dump_optional_str_set(entity.tags)
        model.panel_config = entity.panel_config