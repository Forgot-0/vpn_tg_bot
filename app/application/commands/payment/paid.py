from dataclasses import dataclass
import logging
from typing import Any, Mapping

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.exception import NotFoundException
from app.application.services.payment import BasePaymentService
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.repositories.servers import BaseServerRepository
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository
from app.domain.services.ports import ApiClient
from app.infrastructure.mediator.event import BaseEventBus


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PaidPaymentCommand(BaseCommand):
    playload: dict[str, Any]
    headers: Mapping[str, str]


@dataclass(frozen=True)
class PaidPaymentCommandHandler(BaseCommandHandler[PaidPaymentCommand, str]):
    user_repository: BaseUserRepository
    payment_repository: BasePaymentRepository
    payment_service: BasePaymentService
    subscription_repository: BaseSubscriptionRepository
    server_repository: BaseServerRepository
    api_panel: ApiClient
    event_bus: BaseEventBus

    async def handle(self, command: PaidPaymentCommand) -> None:
        payment_id = await self.payment_service.handle_webhook(
            command.playload, headers=command.playload
        )
        payment = await self.payment_repository.get_by_payment_id(payment_id=str(payment_id))

        if not payment:
            raise NotFoundException()

        user = await self.user_repository.get_by_id(id=payment.user_id)

        if not user:
            raise NotFoundException()

        payment.paid()
        payment.subscription.activate()
        await self.subscription_repository.update(subscription=payment.subscription)

        server = await self.server_repository.get_by_id(server_id=payment.subscription.server_id)
        if not server:
            raise NotFoundException()

        await self.payment_repository.update(payment=payment)

        await self.api_panel.create_or_upgrade_subscription(
            user=user,
            subscription=payment.subscription,
            server=server
        )

        await self.event_bus.publish(payment.pull_events())

        logger.info("Paid payment", extra={"payment": payment})

