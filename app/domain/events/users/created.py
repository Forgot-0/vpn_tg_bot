from dataclasses import dataclass, field
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class NewUserEvent(BaseEvent):
    user_id: UUID
    username: str | None = field(default=None)