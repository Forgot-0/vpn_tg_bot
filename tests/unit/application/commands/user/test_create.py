import pytest

from app.application.commands.users.create import CreateUserCommand, CreateUserCommandHandler



@pytest.mark.asyncio
async def test_create_user_command(
    mock_user_repository,
    mock_event_mediator
) -> None:
    command = CreateUserCommand(
        tg_id=123456,
        is_premium=False,
        username=None,
        fullname=None,
        phone=None,
        referred_by=None
    )

    handler = CreateUserCommandHandler(
        mediator=mock_event_mediator,
        user_repository=mock_user_repository
    )
    await handler.handle(command=command)
    user = await mock_user_repository.get_by_telegram_id(telegram_id=123456)
    assert user is not None
    assert len(mock_event_mediator.published) > 0


@pytest.mark.asyncio
async def test_create_user_command_user_already_exists(
    mock_user_repository,
    mock_event_mediator,
    dummy_user
) -> None:
    await mock_user_repository.create(dummy_user)
    command = CreateUserCommand(
        tg_id=123456,
        is_premium=False,
        username="newuser",
        fullname="New User",
        phone="0987654321",
        referred_by=None
    )
    handler = CreateUserCommandHandler(
        mediator=mock_event_mediator,
        user_repository=mock_user_repository
    )

    await handler.handle(command=command)
    user = await mock_user_repository.get_by_id(dummy_user.id)
    assert user.username is None
    assert len(mock_event_mediator.published) == 0


@pytest.mark.asyncio
async def test_create_user_command_with_full_data(mock_user_repository, mock_event_mediator) -> None:
    referred_uuid_str = "d3b07384-d9a2-4ab4-8b2e-8f0b3b7cf5de"
    command = CreateUserCommand(
        tg_id=789012,
        is_premium=True,
        username="fulluser",
        fullname="Full Name User",
        phone="555123456",
        referred_by=referred_uuid_str
    )
    handler = CreateUserCommandHandler(
        mediator=mock_event_mediator,
        user_repository=mock_user_repository
    )

    await handler.handle(command=command)
    user = await mock_user_repository.get_by_telegram_id(telegram_id=789012)
    assert user is not None
    assert user.username == "fulluser"
    assert user.is_premium is True
    assert user.referred_by.as_generic_type() == referred_uuid_str
    assert len(mock_event_mediator.published) > 0


@pytest.mark.asyncio
async def test_create_user_command_multiple_calls(mock_user_repository, mock_event_mediator) -> None:
    command = CreateUserCommand(
        tg_id=555555,
        is_premium=False,
        username="duplicate",
        fullname="Duplicate User",
        phone="111222333",
        referred_by=None
    )
    handler = CreateUserCommandHandler(
        mediator=mock_event_mediator,
        user_repository=mock_user_repository
    )

    await handler.handle(command=command)
    first_user = await mock_user_repository.get_by_telegram_id(telegram_id=555555)
    assert first_user is not None
    events_count_after_first = len(mock_event_mediator.published)

    await handler.handle(command=command)
    second_user = await mock_user_repository.get_by_telegram_id(telegram_id=555555)
    assert second_user is not None
    assert second_user == first_user
    assert len(mock_event_mediator.published) == events_count_after_first

