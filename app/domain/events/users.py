from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import DomainEvent
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class UserCreatedEvent(DomainEvent):
    __event_name__ = "user.created"

    user_id: UUID
    email: str | None
    telegram_id: int | None
    referred_by: UUID | None


@dataclass(frozen=True)
class UserRoleChangedEvent(DomainEvent):
    __event_name__ = "user.role_changed"

    user_id: UUID
    old_role: UserRole
    new_role: UserRole
