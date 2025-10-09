from dataclasses import dataclass
import logging
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.repositories.payment import BasePaymentRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from infrastructure.api_client.factory import ApiClientFactory
from infrastructure.mediator.event import BaseEventBus


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PaidPaymentCommand(BaseCommand):
    payment_id: UUID


@dataclass(frozen=True)
class PaidPaymentCommandHandler(BaseCommandHandler[PaidPaymentCommand, str]):
    user_repository: BaseUserRepository
    payment_repository: BasePaymentRepository
    subscription_repository: BaseSubscriptionRepository
    server_repository: BaseServerRepository
    api_panel_factory: ApiClientFactory
    event_bus: BaseEventBus 

    async def handle(self, command: PaidPaymentCommand) -> None:
        payment = await self.payment_repository.get_by_payment_id(payment_id=command.payment_id)
        if not payment:
            raise

        user = await self.user_repository.get_by_id(id=payment.user_id)

        if not user: raise

        payment.paid()
        payment.subscription.activate()
        await self.subscription_repository.update(subscription=payment.subscription)

        server = await self.server_repository.get_by_id(server_id=payment.subscription.server_id)
        if not server: raise

        await self.payment_repository.update(payment=payment)

        api_client = self.api_panel_factory.get(server.api_type)
        await api_client.create_or_upgrade_subscription(
            user=user,
            subscription=payment.subscription,
            server=server
        )

        await self.event_bus.publish(payment.pull_events())

        logger.info("Paid payment", extra={"payment": payment})