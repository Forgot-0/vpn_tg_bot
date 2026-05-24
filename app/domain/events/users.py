from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import DomainEvent


@dataclass(frozen=True)
class UserCreatedEvent(DomainEvent):
    __event_name__ = "user.created"

    user_id: UUID
    email: str | None
    telegram_id: int | None


@dataclass(frozen=True)
class UserRoleChangedEvent(DomainEvent):
    __event_name__ = "user.role_changed"

    user_id: UUID
    old_role: str
    new_role: str

