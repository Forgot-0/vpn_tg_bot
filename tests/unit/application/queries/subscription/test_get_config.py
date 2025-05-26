import pytest

from application.queries.subscription.get_config import GetConfigQuery, GetConfigQueryHandler
from domain.values.servers import ProtocolType



@pytest.mark.asyncio
async def test_get_config_query(
    mock_subscription_repository,
    mock_user_repository,
    mock_server_repository,
    protocol_builder_factory,
    dummy_user,
    dummy_server,
    dummy_subscription
):
    await mock_subscription_repository.create(dummy_subscription)
    await mock_user_repository.create(dummy_user)
    await mock_server_repository.create(dummy_server)

    handler = GetConfigQueryHandler(
        subscription_repository=mock_subscription_repository,
        user_repositry=mock_user_repository,
        server_reposiotry=mock_server_repository,
        builder_factory=protocol_builder_factory
    )

    result = await handler.handle(GetConfigQuery(dummy_subscription.id.value))
    assert result
    assert result.protocol_type == ProtocolType.mock