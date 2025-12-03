from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from app.domain.events.base import BaseEvent
# from app.infrastructure.message_broker.base import BaseMessageBroker
# from app.infrastructure.message_broker.convertors import convert_event_to_broker_message


@dataclass(frozen=True)
class IntegrationEvent(BaseEvent, ABC):
    ...


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class BaseEventHandler(ABC, Generic[ET, ER]):

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...


# @dataclass(frozen=True)
# class PublisherEventHandler(BaseEventHandler[BaseEvent, None]):
#     message_broker: BaseMessageBroker
#     broker_topic: str | None = 'game'

#     async def handle(self, event: BaseEvent) -> None:
#         await self.message_broker.send_message(
#             topic=self.broker_topic,
#             value=convert_event_to_broker_message(event=event),
#             key=str(event.event_id).encode(),
#         )