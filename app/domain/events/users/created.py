from dataclasses import dataclass, field

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class NewUserEvent(BaseEvent):
    id: int
    username: str | None = field(default=None)