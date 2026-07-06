from __future__ import annotations

from app.domain.entities.server import VPNServer
from app.domain.values.servers import (
    Capacity,
    FeatureCode,
    Location,
    PanelCredentials,
    PanelEndpoint,
    PanelType,
    ProtocolCode,
)
from app.infrastructure.db.models.server import VPNServerModel


def _dump_enum_values(values: set[FeatureCode] | set[ProtocolCode] | set[str]) -> list[str]:
    return sorted(item if isinstance(item, str) else item.value for item in values)


def _dump_locations(locations: set[Location]) -> list[dict[str, str]]:
    return [
        {"code": location.code, "name": location.name, "flag": location.flag}
        for location in sorted(locations, key=lambda item: item.code)
    ]


def _load_locations(raw: list[dict[str, str]] | None) -> set[Location]:
    if raw is None:
        return set()

    return {
        Location(
            code=item["code"],
            name=item.get("name", ""),
            flag=item.get("flag", ""),
        )
        for item in raw
    }


def _load_protocols(raw: list[str] | None) -> set[ProtocolCode]:
    if not raw:
        return set()
    return {ProtocolCode(item) for item in raw}


def _load_features(raw: list[str] | None) -> set[FeatureCode]:
    if not raw:
        return set()
    return {FeatureCode(item) for item in raw}


class ServerMapper:
    @staticmethod
    def from_server_domain_to_model(server: VPNServer) -> VPNServerModel:
        return VPNServerModel(
            id=server.id,
            name=server.name,
            max_client=server.capacity.max_client,
            free=server.capacity.free,
            panel_type=server.panel_type.value,
            panel_host=server.panel_endpoint.host,
            panel_port=server.panel_endpoint.port,
            panel_path=server.panel_endpoint.path,
            panel_use_ssl=server.panel_endpoint.use_ssl,
            panel_username=server.panel_credentials.username,
            panel_password=server.panel_credentials.password,
            panel_api_token=server.panel_credentials.api_token,
            locations=_dump_locations(server.locations),
            support_protocols=_dump_enum_values(server.support_protocols),
            support_features=_dump_enum_values(server.support_features),
            is_active=server.is_active,
            tags=server.tags,
        )

    @staticmethod
    def from_server_model_to_domain(server_model: VPNServerModel) -> VPNServer:
        return VPNServer(
            id=server_model.id,
            name=server_model.name,
            capacity=Capacity(max_client=server_model.max_client, free=server_model.free),
            panel_type=PanelType(server_model.panel_type),
            panel_endpoint=PanelEndpoint(
                host=server_model.panel_host,
                port=server_model.panel_port,
                path=server_model.panel_path,
                use_ssl=server_model.panel_use_ssl,
            ),
            panel_credentials=PanelCredentials(
                username=server_model.panel_username,
                password=server_model.panel_password,
                api_token=server_model.panel_api_token,
            ),
            locations=_load_locations(server_model.locations),
            support_protocols=_load_protocols(server_model.support_protocols),
            support_features=_load_features(server_model.support_features),
            is_active=server_model.is_active,
            tags=server_model.tags or [],
        )
