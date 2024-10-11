from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.repositories.servers.base import BaseServerRepository


@dataclass(frozen=True)
class UpdateCurrentServerEventHandler(BaseEventHandler[PaidSubscriptionEvent, None]):
    server_repository: BaseServerRepository

    async def handle(self, event: PaidSubscriptionEvent) -> None:
        ...