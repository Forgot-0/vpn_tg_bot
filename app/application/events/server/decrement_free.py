from dataclasses import dataclass

from app.application.events.base import BaseEventHandler
from app.domain.events.paymens.paid import PaidPaymentEvent
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.repositories.servers import BaseServerRepository



@dataclass(frozen=True)
class DecrementFreeServerEventHandler(BaseEventHandler[PaidPaymentEvent, None]):
    payment_repository: BasePaymentRepository
    server_repository: BaseServerRepository

    async def handle(self, event: PaidPaymentEvent) -> None:
        payment = await self.payment_repository.get_by_id(id=event.order_id)
        if not payment: raise
        await self.server_repository.update_decrement_free(
            server_id=payment.subscription.server_id,
            decr=payment.subscription.device_count
        )