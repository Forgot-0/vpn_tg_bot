from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.repositories.users.base import BaseUserRepository
from infra.vpn_service.base import BaseVpnService
from infra.vpn_service.schema import Client, CreateVpnUrl, Settings


@dataclass(frozen=True)
class PaidSubscriptionEventHandler(BaseEventHandler[PaidSubscriptionEvent, None]):
    user_repository: BaseUserRepository
    vpn_servise: BaseVpnService

    async def handle(self, event: PaidSubscriptionEvent) -> None:
        user = await self.user_repository.get_by_tg_id(tg_id=event.tg_id)
        if not user.vpn_url:
            data = CreateVpnUrl(
                id=1,
                settings=Settings(
                    clients=[
                        Client(
                            id=str(user.id),
                            email=str(event.tg_id),
                            tg_id=event.tg_id,
                            expiryTime=(int(event.end_time.timestamp())+60)*1000
                        )
                    ]
                )
            )
            await self.vpn_servise.create(data=data)

        else:
            client = await self.vpn_servise.get_by_id(id=user.id)
            client.expiryTime += event.end_time - event.created_at
            await self.vpn_servise.udate(data=client)
