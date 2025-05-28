from uuid import uuid4
import pytest

from application.commands.payment.paid import PaidPaymentCommand, PaidPaymentCommandHandler
from domain.entities.payment import Payment, PaymentStatus


@pytest.mark.asyncio
async def test_paid_order_command_handler(
    mock_user_repository,
    mock_payment_repository,
    mock_server_repository,
    mock_subscription_repository,
    api_client_factory,
    dummy_user,
    dummy_subscription,
    dummy_server,
    mock_event_mediator,
    mock_telegram_bot,
    subs_price_service
):
    mock_bot = mock_telegram_bot

    order = Payment.create(
        subscription=dummy_subscription,
        user_id=dummy_user.id,
        discount=None,
        price=subs_price_service.calculate(dummy_subscription)
    )
    order.payment_id = uuid4()
    order.status = PaymentStatus.pending

    mock_payment_repository._data[order.payment_id] = order
    mock_user_repository._data[dummy_user.id] = dummy_user
    mock_server_repository._data[dummy_server.id] = dummy_server

    command = PaidPaymentCommand(payment_id=order.payment_id)

    handler = PaidPaymentCommandHandler(
        user_repository=mock_user_repository,
        payment_repository=mock_payment_repository,
        server_repository=mock_server_repository,
        subscription_repository=mock_subscription_repository,
        api_panel_factory=api_client_factory,
        bot=mock_bot,
        mediator=mock_event_mediator
    )

    ret = await handler.handle(command)
    updated_order = await mock_payment_repository.get_by_payment_id(order.payment_id)
    assert updated_order.status == PaymentStatus.succese
    assert await mock_subscription_repository.get_by_id(id=order.subscription.id)
    assert len(mock_bot.data) > 0

@pytest.mark.asyncio
async def test_paid_order_command_handler_payment_not_found(
    mock_user_repository,
    mock_payment_repository,
    mock_server_repository,
    mock_subscription_repository,
    api_client_factory,
    mock_event_mediator,
    mock_telegram_bot,
):
    non_existent_payment_id = uuid4()
    command = PaidPaymentCommand(payment_id=non_existent_payment_id)
    handler = PaidPaymentCommandHandler(
        user_repository=mock_user_repository,
        payment_repository=mock_payment_repository,
        server_repository=mock_server_repository,
        subscription_repository=mock_subscription_repository,
        api_panel_factory=api_client_factory,
        bot=mock_telegram_bot,
        mediator=mock_event_mediator
    )
    with pytest.raises(Exception):
        await handler.handle(command)



