from app.domain.entities.server import VPNServer
from app.domain.values.servers import PanelConfig, PanelCredentials,  PanelType, ProtocolCode
from app.domain.values.subscriptions import PlanFeatureCode
from app.infrastructure.db.models.servers import VPNServerModel


class VPNServerMapper:
    @staticmethod
    def to_domain(model: VPNServerModel) -> VPNServer:
        config = PanelConfig(
            host=model.panel_ip,
            panel_port=model.panel_port,
            panel_path=model.panel_path,
            domain=model.panel_domain,
        )
        credits_ = PanelCredentials(
            username=model.panel_username,
            password=model.panel_password,
            two_factor_code=model.panel_two_factor_code,
        )
        return VPNServer(
            id=model.id,
            panel_type=PanelType(model.panel_type),
            panel_config=config,
            panel_credentials=credits_,
            region_code=model.region_code,
            is_active=model.is_active,
            supported_protocols=frozenset(
                ProtocolCode(p) for p in model.supported_protocols
            ),
            supported_features=frozenset(
                PlanFeatureCode(f) for f in model.supported_features
            ),
            protocols_config={ProtocolCode(key): value for key, value in model.protocols_config.items()}
        )

    @staticmethod
    def to_model(entity: VPNServer) -> VPNServerModel:
        return VPNServerModel(
            id=entity.id,
            panel_type=entity.panel_type.value,
            panel_ip=entity.panel_config.host,
            panel_port=entity.panel_config.panel_port,
            panel_path=entity.panel_config.panel_path,
            panel_domain=entity.panel_config.domain,
            panel_username=entity.panel_credentials.username,
            panel_password=entity.panel_credentials.password,
            panel_two_factor_code=entity.panel_credentials.two_factor_code,
            region_code=entity.region_code,
            is_active=entity.is_active,
            supported_protocols=[p.value for p in entity.supported_protocols],
            supported_features=[f.value for f in entity.supported_features],
            protocols_config={key.value: value for key, value in entity.protocols_config.items()}
        )

    @staticmethod
    def update_model(model: VPNServerModel, entity: VPNServer) -> None:
        model.panel_type = entity.panel_type.value
        model.panel_ip = entity.panel_config.host
        model.panel_port = entity.panel_config.panel_port
        model.panel_path = entity.panel_config.panel_path
        model.panel_domain = entity.panel_config.domain
        model.panel_username = entity.panel_credentials.username
        model.panel_password = entity.panel_credentials.password
        model.panel_two_factor_code = entity.panel_credentials.two_factor_code
        model.region_code = entity.region_code
        model.is_active = entity.is_active
        model.supported_protocols = [p.value for p in entity.supported_protocols]
        model.supported_features = [f.value for f in entity.supported_features]
        model.protocols_config = {key.value: value for key, value in entity.protocols_config.items()}
