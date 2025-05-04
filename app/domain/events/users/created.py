from dataclasses import dataclass, field

from domain.events.base import BaseEvent
from domain.values.users import UserId


@dataclass(frozen=True)
class NewUserEvent(BaseEvent):
    user_id: UserId
    username: str | None = field(default=None)