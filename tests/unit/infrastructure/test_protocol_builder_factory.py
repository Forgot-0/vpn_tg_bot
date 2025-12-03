from app.domain.values.servers import ApiType, ProtocolType, VPNConfig
from app.infrastructure.builders_params.factory import ProtocolBuilderFactory
from app.domain.entities.server import ProtocolConfig


def test_protocol_builder_factory(
    protocol_builder_factory: ProtocolBuilderFactory,
    dummy_user,
    dummy_subscription,
    dummy_server
):
    dummy_config = ProtocolConfig(
        protocol_type=ProtocolType.mock,
        config={"dummy": "value"}
    )
    dummy_api_type = ApiType.mock
    builder = protocol_builder_factory.get(dummy_api_type, dummy_config.protocol_type)
    params = builder.build_params(dummy_user, dummy_subscription, dummy_server)
    config_vpn = builder.builde_config_vpn(dummy_user, dummy_subscription, dummy_server)
    assert isinstance(params, dict)
    assert isinstance(config_vpn, VPNConfig)
