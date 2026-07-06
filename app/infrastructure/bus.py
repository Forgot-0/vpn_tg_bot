from collections.abc import Iterable
from dataclasses import dataclass

from dishka import AsyncContainer

from app.application.event_bus import EventBus
from app.domain.events.base import DomainEvent



@dataclass(eq=False)
class MediatorEventBus(EventBus):
    container: AsyncContainer

    async def publish(self, events: Iterable[DomainEvent]) -> None:
        for event in events:
            type_handlers = self.event_registy.get_handler_types([event])
            if not type_handlers:
                continue

            for type_handler in type_handlers:
                async with self.container() as requests_container:
                    handler = await requests_container.get(type_handler)
                    await handler.handle(event)
