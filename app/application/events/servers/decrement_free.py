from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.orders.paid import PaidOrderEvent
from domain.repositories.servers import BaseServerRepository


@dataclass(frozen=True)
class UpdateCurrentServerEventHandler(BaseEventHandler[PaidOrderEvent, None]):
    server_repository: BaseServerRepository

    async def handle(self, event: PaidOrderEvent) -> None:
        await self.server_repository.update_decrement_free(server_id=event.server_id)