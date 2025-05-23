
import logging

from application.events.base import BaseEventHandler
from domain.events.base import BaseEvent


logger = logging.getLogger(__name__)


class LogHandlerEvent(BaseEventHandler[BaseEvent, None]):
    async def handle(self, event: BaseEvent) -> None:
        logger.info(f"Event {event.__class__.__name__}", extra={"data": event})