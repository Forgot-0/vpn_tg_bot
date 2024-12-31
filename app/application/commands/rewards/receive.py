from dataclasses import dataclass
from uuid import UUID

from aiogram import Bot

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.order import Order
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.users import BaseUserRepository
from domain.services.rewards import RewardService
from infrastructure.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class ReceiveRewardCommand(BaseCommand):
    user_id: int
    reward_id: UUID


@dataclass(frozen=True)
class ReceiveRewardCommandHandler(BaseCommandHandler[ReceiveRewardCommand, None]):
    user_repository: BaseUserRepository
    reward_service: RewardService
    order_repository: BaseOrderRepository
    server_repository: BaseServerRepository
    vpn_service: BaseVpnService
    bot: Bot

    async def handle(self, command: ReceiveRewardCommand) -> None:
        reward = await self.reward_service.receive_reward(
            user_id=command.user_id,
            reward_id=command.reward_id
        )

        user = await self.user_repository.get_by_id(id=command.user_id)
        server = await self.server_repository.get_by_id(user.server_id)

        order = Order.create(
            subscription=reward.present,
            user_id=command.user_id,
        )

        await self.order_repository.create(order=order)
        await self.order_repository.pay(id=order.id)

        url = await self.vpn_service.create(id=user.uuid, subscription=order.subscription, server=server)
        await self.bot.send_message(chat_id=order.user_id, text=f"`{url}`", parse_mode='MarkdownV2')

        await self.mediator.publish(reward.pull_events())

