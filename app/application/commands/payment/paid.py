from dataclasses import dataclass
import logging
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.repositories.payment import BasePaymentRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.values.servers import VPNConfig
from infrastructure.api_client.factory import ApiClientFactory
from infrastructure.tgbot.base import BaseTelegramBot


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
    bot: BaseTelegramBot

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
        vpn_configs = await api_client.create_or_upgrade_subscription(user=user, subscription=payment.subscription, server=server)

        if user.telegram_id:
            await self.bot.send_vpn_configs(user.telegram_id, vpn_configs=vpn_configs)

        await self.mediator.publish(payment.pull_events())

        logger.info("Paid order", extra={"order": payment})