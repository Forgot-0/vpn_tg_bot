import pytest

from application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from application.dtos.payments.url import PaymentDTO
from domain.values.servers import ProtocolType


@pytest.mark.asyncio
async def test_create_subscription_command_handler(
    mock_subscription_repository,
    mock_user_repository,
    mock_order_repository,
    mock_server_repository,
    mock_payment_service,
    subs_price_service,
    mock_event_mediator,
    dummy_user,
    dummy_subscription,
    dummy_server,
):
    mock_server_repository._data[dummy_server.id] = dummy_server
    mock_user_repository._data[dummy_user.id] = dummy_user

    command = CreateSubscriptionCommand(
        telegram_id=dummy_user.telegram_id,
        duration=dummy_subscription.duration,
        device_count=dummy_subscription.device_count,
        protocol_types=[ProtocolType.mock.value],
    )

    handler = CreateSubscriptionCommandHandler(
        user_repository=mock_user_repository,
        subscription_repository=mock_subscription_repository,
        order_repository=mock_order_repository,
        server_repository=mock_server_repository,
        payment_service=mock_payment_service,
        subs_price_service=subs_price_service,
        mediator=mock_event_mediator
    )

    result: PaymentDTO = await handler.handle(command)
    assert isinstance(result, PaymentDTO)
    assert result.url.startswith("http://")
    assert len(await mock_subscription_repository.get_by_user(dummy_user.id)) == 1