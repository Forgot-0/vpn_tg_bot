from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.orders.paid import PaidOrderEvent
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository



@dataclass(frozen=True)
class DecrementFreeServerEventHandler(BaseEventHandler[PaidOrderEvent, None]):
    order_repository: BaseOrderRepository
    server_repository: BaseServerRepository

    async def handle(self, event: PaidOrderEvent) -> None:
        order = await self.order_repository.get_by_id(id=event.order_id)
        if not order: raise
        await self.server_repository.update_decrement_free(
            server_id=order.subscription.server_id,
            decr=order.subscription.device_count
        )