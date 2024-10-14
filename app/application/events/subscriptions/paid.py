from dataclasses import dataclass

from aiogram import Bot

from application.events.base import BaseEventHandler
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.repositories.servers.base import BaseServerRepository
from infra.repositories.subscriptions.base import BaseSubscriptionRepository
from infra.vpn_service.base import BaseVpnService


@dataclass(frozen=True)
class PaidSubscriptionEventHandler(BaseEventHandler[PaidSubscriptionEvent, None]):
    subscription_repository: BaseSubscriptionRepository
    server_reposiptory: BaseServerRepository
    vpn_servise: BaseVpnService
    bot: Bot

    async def handle(self, event: PaidSubscriptionEvent) -> None:
        server = await self.server_reposiptory.get_by_id(server_id=event.server_id)
        url = await self.vpn_servise.create(
            event=event,
            server=server
        )
        await self.bot.send_message(chat_id=event.tg_id, text=f'`{url}`', parse_mode='MarkdownV2')
        await self.subscription_repository.set_vpn_url(subs_id=event.subscription_id, vpn_url=url)
