from app.domain.entities.server import VPNServer
from app.domain.values.servers import (
    FeatureCode,
    PanelCredentials,
    PanelEndpoint,
    PanelType,
    ProtocolCode,
)
from app.infrastructure.db.mappers._serialization import dump_enum_set, dump_optional_str_set, load_enum_set
from app.infrastructure.db.models.servers import VPNServerModel


class VPNServerMapper:
    @staticmethod
    def to_entity(model: VPNServerModel) -> VPNServer:
        return VPNServer(
            id=model.id,
            name=model.name,
            region_code=model.region_code,
            panel_type=PanelType(model.panel_type),
            panel_endpoint=PanelEndpoint(
                host=model.panel_host,
                port=model.panel_port,
                path=model.panel_path,
                use_ssl=model.panel_use_ssl,
            ),
            panel_credentials=PanelCredentials(
                username=model.panel_username,
                password=model.panel_password,
                api_token=model.panel_two_factor_secret,
            ),
            supported_protocols=load_enum_set(model.supported_protocols, ProtocolCode),
            supported_features=load_enum_set(model.supported_features, FeatureCode),
            is_active=model.is_active,
            max_clients=model.max_clients,
            current_clients=model.current_clients,
            tags=frozenset(model.tags or []),
        )

    @staticmethod
    def to_model(entity: VPNServer) -> VPNServerModel:
        return VPNServerModel(
            id=entity.id,
            name=entity.name,
            region_code=entity.region_code,
            panel_type=entity.panel_type.value,
            panel_host=entity.panel_endpoint.host,
            panel_port=entity.panel_endpoint.port,
            panel_path=entity.panel_endpoint.path,
            panel_use_ssl=entity.panel_endpoint.use_ssl,
            panel_username=entity.panel_credentials.username,
            panel_password=entity.panel_credentials.password,
            panel_two_factor_secret=entity.panel_credentials.api_token,
            supported_protocols=dump_enum_set(entity.supported_protocols),
            supported_features=dump_enum_set(entity.supported_features),
            is_active=entity.is_active,
            max_clients=entity.max_clients,
            current_clients=entity.current_clients,
            tags=dump_optional_str_set(entity.tags),
        )

    @staticmethod
    def update_model(model: VPNServerModel, entity: VPNServer) -> None:
        model.name = entity.name
        model.region_code = entity.region_code
        model.panel_type = entity.panel_type.value
        model.panel_host = entity.panel_endpoint.host
        model.panel_port = entity.panel_endpoint.port
        model.panel_path = entity.panel_endpoint.path
        model.panel_use_ssl = entity.panel_endpoint.use_ssl
        model.panel_username = entity.panel_credentials.username
        model.panel_password = entity.panel_credentials.password
        model.panel_two_factor_secret = entity.panel_credentials.api_token
        model.supported_protocols = dump_enum_set(entity.supported_protocols)
        model.supported_features = dump_enum_set(entity.supported_features)
        model.is_active = entity.is_active
        model.max_clients = entity.max_clients
        model.current_clients = entity.current_clients
        model.tags = dump_optional_str_set(entity.tags)
