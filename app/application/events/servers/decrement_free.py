from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.orders.paid import PaidOrderEvent
from domain.repositories.servers import BaseServerRepository
from domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class UpdateCurrentServerEventHandler(BaseEventHandler[PaidOrderEvent, None]):
    user_repository: BaseUserRepository
    server_repository: BaseServerRepository

    async def handle(self, event: PaidOrderEvent) -> None:
        user = await self.user_repository.get_by_id(id=event.user_id)
        await self.server_repository.update_decrement_free(server_id=user.id)