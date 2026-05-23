from dataclasses import dataclass, field
from uuid import UUID

from app.domain.events.base import BaseEvent


@dataclass(frozen=True)
class NewUserEvent(BaseEvent):
    user_id: UUID
    email: str | None
    telegram_id: int | None

