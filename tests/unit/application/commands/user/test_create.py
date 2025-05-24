import pytest

from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler



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
