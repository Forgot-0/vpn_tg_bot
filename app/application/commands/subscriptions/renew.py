from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.subscriptions import RenewSubscriptionResultDTO
from app.application.event_bus import EventBus
from app.application.interfaces.servers import PanelClientFactory
from app.domain.errors import (
    CheckoutNotFoundError,
    PanelConnectionInactiveError,
    PanelConnectionNotFoundError,
    PaymentNotFoundError,
    ProvisioningFailedError,
    ServerNotFoundError,
    SubscriptionNotFoundError,
    SubscriptionNotRenewableError,
)
from app.domain.repositories.access import ProvisionedAccessRepository
from app.domain.repositories.checkouts import CheckoutSessionRepository
from app.domain.repositories.panel_connections import PanelConnectionRepository
from app.domain.repositories.payments import PaymentIntentRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.values.checkouts import CheckoutIntent
from app.domain.values.payments import PaymentStatus
from app.domain.values.subscriptions import ProvisioningStatus, SubscriptionStatus


@dataclass(frozen=True)
class RenewSubscriptionCommand(BaseCommand):
    subscription_id: UUID
    payment_intent_id: UUID
    renewed_at: datetime
    external_payment_id: str | None = None


@dataclass(frozen=True)
class RenewSubscriptionHandler(
    BaseCommandHandler[RenewSubscriptionCommand, RenewSubscriptionResultDTO]
):
    subscription_repository: SubscriptionRepository
    payment_repository: PaymentIntentRepository
    checkout_repository: CheckoutSessionRepository
    server_repository: VPNServerRepository
    connection_repository: PanelConnectionRepository
    access_repository: ProvisionedAccessRepository
    panel_factory: PanelClientFactory
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: RenewSubscriptionCommand) -> RenewSubscriptionResultDTO:
        payment_intent = await self.payment_repository.get_by_id(command.payment_intent_id)
        if payment_intent is None:
            raise PaymentNotFoundError(entity_id=str(command.payment_intent_id))

        if payment_intent.status != PaymentStatus.SUCCEEDED:
            if command.external_payment_id is None:
                raise PaymentNotFoundError(entity_id=str(command.payment_intent_id))
            payment_intent.succeed(
                external_id=command.external_payment_id,
                paid_at=command.renewed_at,
            )

        if payment_intent.checkout_session_id is None:
            raise CheckoutNotFoundError(entity_id=str(command.payment_intent_id))

        checkout = await self.checkout_repository.get_by_id(payment_intent.checkout_session_id)
        if checkout is None:
            raise CheckoutNotFoundError(entity_id=str(payment_intent.checkout_session_id))

        if checkout.metadata.get("intent") != CheckoutIntent.RENEWAL.value:
            raise CheckoutNotFoundError(entity_id=str(checkout.id))

        checkout_subscription_id = checkout.metadata.get("subscription_id")
        if checkout_subscription_id != str(command.subscription_id):
            raise SubscriptionNotFoundError(entity_id=str(command.subscription_id))

        subscription = await self.subscription_repository.get_by_id(command.subscription_id)
        if subscription is None:
            raise SubscriptionNotFoundError(entity_id=str(command.subscription_id))

        if subscription.status not in {
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.EXPIRED,
        }:
            raise

        if subscription.spec.is_time_limited is False:
            raise SubscriptionNotRenewableError(
                reason="Only time-limited subscriptions can be renewed",
            )

        if subscription.server_id is None:
            raise SubscriptionNotRenewableError(
                reason="Subscription has no associated server",
            )

        previous_expires_at = subscription.expires_at
        duration_days = checkout.spec.duration_days

        server = await self.server_repository.get_by_id(subscription.server_id)
        if server is None:
            raise ServerNotFoundError(entity_id=str(subscription.server_id))

        connection = await self.connection_repository.get_by_id(server.panel_connection_id)
        if connection is None:
            raise PanelConnectionNotFoundError(entity_id=str(server.panel_connection_id))

        if not connection.is_active:
            raise PanelConnectionInactiveError

        accesses = await self.access_repository.list_by_subscription(subscription.id)
        active_access = next(
            (item for item in reversed(accesses) if item.status == ProvisioningStatus.ACTIVE),
            accesses[-1] if accesses else None,
        )

        subscription.renew(
            renewed_at=command.renewed_at,
            duration_days=duration_days,
        )

        if active_access is not None:
            panel_client = self.panel_factory.get_client(connection)
            try:
                await panel_client.renew(
                    server=server,
                    connection=connection,
                    subscription=subscription,
                    access=active_access,
                )
            except Exception as exc:
                await self.uow.rollback()
                raise ProvisioningFailedError(reason=str(exc)) from exc

        checkout.mark_converted(payment_intent.id)

        await self.payment_repository.update(payment_intent)
        await self.subscription_repository.update(subscription)
        await self.checkout_repository.update(checkout)
        await self.uow.commit()

        await self.event_bus.publish(payment_intent.pull_events())
        await self.event_bus.publish(checkout.pull_events())
        await self.event_bus.publish(subscription.pull_events())

        return RenewSubscriptionResultDTO.create(
            subscription=subscription,
            previous_expires_at=previous_expires_at,
            new_expires_at=subscription.expires_at,
        )
