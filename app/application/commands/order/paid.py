from dataclasses import dataclass
import logging
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.users import BaseUserRepository
from domain.values.servers import VPNConfig
from infrastructure.api_client.factory import ApiClientFactory
from infrastructure.tgbot.base import BaseTelegramBot


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PaidOrderCommand(BaseCommand):
    payment_id: UUID


@dataclass(frozen=True)
class PaidOrderCommandHandler(BaseCommandHandler[PaidOrderCommand, str]):
    user_repository: BaseUserRepository
    order_repository: BaseOrderRepository
    server_repository: BaseServerRepository
    api_panel_factory: ApiClientFactory
    bot: BaseTelegramBot

    async def handle(self, command: PaidOrderCommand) -> None:
        order = await self.order_repository.get_by_payment_id(payment_id=command.payment_id)
        if not order:
            raise

        user = await self.user_repository.get_by_id(id=order.user_id)

        if not user: raise

        order.paid()
        server = await self.server_repository.get_by_id(server_id=order.subscription.server_id)

        if not server: raise

        await self.order_repository.update(order=order)

        api_client = self.api_panel_factory.get(server.api_type)
        vpn_configs = await api_client.create_subscription(user=user, subscription=order.subscription, server=server)


        if user.telegram_id:
            await self.bot.send_vpn_configs(user.telegram_id, vpn_configs=vpn_configs)

        await self.mediator.publish(order.pull_events())

        logger.info("Paid order", extra={"order": order})