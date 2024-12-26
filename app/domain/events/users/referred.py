from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class ReferredUserEvent(BaseEvent):
    reffered_by: int