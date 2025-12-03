import pytest

from app.application.queries.subscription.get_by_tgid import GetByTgIdQuery, GetByTgIdQueryHandler



@pytest.mark.asyncio
async def test_get_by_telegram_id_query(
    mock_subscription_repository,
    mock_user_repository,
    dummy_subscription,
    dummy_user
) -> None:
    await mock_user_repository.create(dummy_user)
    await mock_subscription_repository.create(dummy_subscription)
    handler = GetByTgIdQueryHandler(
        user_repository=mock_user_repository,
        subscription_repository=mock_subscription_repository,
    )

    result = await handler.handle(GetByTgIdQuery(dummy_user.telegram_id))

    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_by_telegram_id_query_not_found_user(
    mock_subscription_repository,
    mock_user_repository,
    dummy_subscription,
    dummy_user
) -> None:
    await mock_subscription_repository.create(dummy_subscription)
    handler = GetByTgIdQueryHandler(
        user_repository=mock_user_repository,
        subscription_repository=mock_subscription_repository,
    )

    with pytest.raises(Exception):
        await handler.handle(GetByTgIdQuery(dummy_user.telegram_id))

@pytest.mark.asyncio
async def test_get_by_telegram_id_query_not_found_subscription(
    mock_subscription_repository,
    mock_user_repository,
    dummy_user
) -> None:
    await mock_user_repository.create(dummy_user)
    handler = GetByTgIdQueryHandler(
        user_repository=mock_user_repository,
        subscription_repository=mock_subscription_repository,
    )

    result = await handler.handle(GetByTgIdQuery(dummy_user.telegram_id))
    assert len(result) == 0