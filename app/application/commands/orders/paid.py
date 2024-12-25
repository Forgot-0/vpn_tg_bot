from dataclasses import dataclass
from uuid import UUID

from aiogram import Bot

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from infrastructure.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class PayOrderCommand(BaseCommand):
    order_id: UUID


@dataclass(frozen=True)
class PayOrderCommandHandler(BaseCommandHandler[PayOrderCommand, None]):
    order_repository: BaseOrderRepository
    vpn_service: BaseVpnService
    server_repository: BaseServerRepository
    bot: Bot

    async def handle(self, command: PayOrderCommand) -> None:
        order = await self.order_repository.get_by_id(id=command.order_id)
        if order is None:
            raise

        await self.order_repository.pay(id=order.id)
        order.paid()

        server = await self.server_repository.get_by_id(server_id=order.server_id)
        url = await self.vpn_service.create(order_id=order.id, subscription=order.subscription, server=server)
        await self.bot.send_message(chat_id=order.user_id, text=f"`{url}`", parse_mode='MarkdownV2')

        await self.mediator.publish(order.pull_events())
