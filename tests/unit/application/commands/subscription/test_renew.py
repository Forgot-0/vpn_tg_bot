from datetime import datetime, timedelta
from uuid import uuid4, UUID
import pytest
from app.application.commands.subscriptions.renew import RenewSubscriptionCommand, RenewSubscriptionCommandHandler
from app.application.dtos.payments.url import PaymentDTO
from app.domain.entities.subscription import SubscriptionStatus
from app.domain.services.utils import now_utc



@pytest.mark.asyncio
async def test_renew_subscription_command_handler_active(
    mock_subscription_repository,
    mock_payment_repository,
    mock_user_repository,
    mock_server_repository,
    subs_price_service,
    mock_payment_service,
    mock_event_mediator,
    dummy_subscription,
):
    dummy_subscription.status = SubscriptionStatus.ACTIVE
    mock_subscription_repository._data[dummy_subscription.id] = dummy_subscription

    command = RenewSubscriptionCommand(subscription_id=dummy_subscription.id.value, duration=30)
    handler = RenewSubscriptionCommandHandler(
        user_repository=mock_user_repository,
        payment_repository=mock_payment_repository,
        server_repository=mock_server_repository,
        subscription_repository=mock_subscription_repository,
        subs_price_service=subs_price_service,
        payment_service=mock_payment_service,
        mediator=mock_event_mediator
    )

    result = await handler.handle(command)
    subscription = await mock_subscription_repository.get_by_id(dummy_subscription.id)

    assert isinstance(result, PaymentDTO)
    assert result.url.startswith("http://")
    assert result.price == 99.0
    assert subscription
    assert subscription.duration == 60
    payment = await mock_payment_repository.get_by_payment_id(UUID("11111111-1111-1111-1111-111111111111"))
    assert payment is not None


@pytest.mark.asyncio
async def test_renew_subscription_command_handler_expired(
    mock_subscription_repository,
    mock_payment_repository,
    mock_user_repository,
    mock_server_repository,
    subs_price_service,
    mock_payment_service,
    mock_event_mediator,
    dummy_subscription
):
    dummy_subscription.status = SubscriptionStatus.EXPIRED
    dummy_subscription.start_date = now_utc() - timedelta(days=31)
    mock_subscription_repository._data[dummy_subscription.id] = dummy_subscription

    new_duration = 30
    command = RenewSubscriptionCommand(subscription_id=dummy_subscription.id.value, duration=new_duration)
    handler = RenewSubscriptionCommandHandler(
        user_repository=mock_user_repository,
        payment_repository=mock_payment_repository,
        server_repository=mock_server_repository,
        subscription_repository=mock_subscription_repository,
        subs_price_service=subs_price_service,
        payment_service=mock_payment_service,
        mediator=mock_event_mediator
    )

    result = await handler.handle(command)
    subscription = await mock_subscription_repository.get_by_id(dummy_subscription.id)

    assert isinstance(result, PaymentDTO)
    assert result.url.startswith("http://")
    assert result.price == 99.0
    assert subscription
    assert subscription.duration == new_duration
    payment = await mock_payment_repository.get_by_payment_id(UUID("11111111-1111-1111-1111-111111111111"))
    assert payment is not None


@pytest.mark.asyncio
async def test_renew_subscription_command_handler_subscription_not_found(
    mock_subscription_repository,
    mock_payment_repository,
    mock_user_repository,
    mock_server_repository,
    subs_price_service,
    mock_payment_service,
    mock_event_mediator
):
    unknown_subscription_id = uuid4()

    command = RenewSubscriptionCommand(subscription_id=unknown_subscription_id, duration=10)
    handler = RenewSubscriptionCommandHandler(
        user_repository=mock_user_repository,
        payment_repository=mock_payment_repository,
        server_repository=mock_server_repository,
        subscription_repository=mock_subscription_repository,
        subs_price_service=subs_price_service,
        payment_service=mock_payment_service,
        mediator=mock_event_mediator
    )

    with pytest.raises(Exception):
        await handler.handle(command)