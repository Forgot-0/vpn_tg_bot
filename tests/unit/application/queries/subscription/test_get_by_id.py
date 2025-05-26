from uuid import uuid4
import pytest

from application.queries.subscription.get_by_id import GetByIdQuery, GetByIdQueryHandler


@pytest.mark.asyncio
async def test_get_by_id_query(
    mock_subscription_repository,
    dummy_subscription,
) -> None:
    await mock_subscription_repository.create(dummy_subscription)

    handler = GetByIdQueryHandler(
        subscription_repository=mock_subscription_repository
    )

    result = await handler.handle(GetByIdQuery(subscription_id=dummy_subscription.id.value))
    assert result


@pytest.mark.asyncio
async def test_get_by_id_query_not_found(
    mock_subscription_repository,
) -> None:
    unknow_subscription_id = uuid4()
    handler = GetByIdQueryHandler(
        subscription_repository=mock_subscription_repository
    )
    with pytest.raises(Exception):
        await handler.handle(GetByIdQuery(subscription_id=unknow_subscription_id))