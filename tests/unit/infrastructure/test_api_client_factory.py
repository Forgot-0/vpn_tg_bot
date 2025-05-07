import pytest
from domain.values.servers import ApiType
from infrastructure.api_client.factory import ApiClientFactory


@pytest.mark.asyncio
async def test_api_client_factory(
    api_client_factory: ApiClientFactory,
    dummy_user,
    dummy_subscription,
    dummy_server
):
    dummy_api_type = ApiType.mock
    client = api_client_factory.get(dummy_api_type)
    result = await client.create_subscription(dummy_user, dummy_subscription, dummy_server)
    assert isinstance(result, list)
