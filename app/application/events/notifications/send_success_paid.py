
from dataclasses import asdict, dataclass

import orjson

from app.application.events.base import BaseEventHandler
from app.domain.events.paymens.paid import PaidPaymentEvent
from app.infrastructure.message_brokers.base import BaseMessageBroker


@dataclass(frozen=True)
class SendMessageTelegramEventHandler(BaseEventHandler[PaidPaymentEvent, None]):
    message_broker: BaseMessageBroker

    async def handle(self, event: PaidPaymentEvent) -> None:
        await self.message_broker.send_message(
            key=str(event.order_id),
            topic=event.get_name(),
            value=orjson.dumps(asdict(event))
        )
