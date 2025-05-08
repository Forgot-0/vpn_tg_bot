from uuid import uuid4
import pytest

from application.commands.order.paid import PaidOrderCommand, PaidOrderCommandHandler
from domain.entities.order import Order, PaymentStatus


@pytest.mark.asyncio
async def test_paid_order_command_handler(
    mock_user_repository,
    mock_order_repository,
    mock_server_repository,
    api_client_factory,
    dummy_user,
    dummy_subscription,
    dummy_server,
    mock_event_mediator,
    mock_telegram_bot
):
    mock_bot = mock_telegram_bot

    order = Order.create(
        subscription=dummy_subscription,
        user_id=dummy_user.id,
        discount=None
    )
    order.payment_id = uuid4()
    order.status = PaymentStatus.pending

    mock_order_repository._data[order.payment_id] = order
    mock_user_repository._data[dummy_user.id] = dummy_user
    mock_server_repository._data[dummy_server.id] = dummy_server

    command = PaidOrderCommand(payment_id=order.payment_id)

    handler = PaidOrderCommandHandler(
        user_repository=mock_user_repository,
        order_repository=mock_order_repository,
        server_repository=mock_server_repository,
        api_panel_factory=api_client_factory,
        bot=mock_bot,
        mediator=mock_event_mediator
    )

    ret = await handler.handle(command)
    updated_order = await mock_order_repository.get_by_payment_id(order.payment_id)
    assert updated_order.status == PaymentStatus.succese

    assert len(mock_bot.data) > 0