from dataclasses import dataclass

from aiogram import Bot

from application.events.base import BaseEventHandler
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.repositories.servers.base import BaseServerRepository
from infra.repositories.users.base import BaseUserRepository
from infra.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class PaidSubscriptionEventHandler(BaseEventHandler[PaidSubscriptionEvent, None]):
    user_repository: BaseUserRepository
    server_reposiptry: BaseServerRepository
    vpn_servise: BaseVpnService
    bot: Bot

    async def handle(self, event: PaidSubscriptionEvent) -> None:
        user = await self.user_repository.get_by_tg_id(tg_id=event.tg_id)
        server = await self.server_reposiptry.get_by_max_free()
        url = await self.vpn_servise.create(
            user_id=user.id,
            event=event,
            server=server
        )
        await self.server_reposiptry.update_decrement_free(server_id=server.id)
        await self.bot.send_message(chat_id=event.tg_id, text=url)