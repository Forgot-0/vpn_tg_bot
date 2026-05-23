from dataclasses import dataclass, field
from uuid import UUID

from app.domain.events.base import BaseEvent


 
@dataclass(frozen=True)
class NewUserEvent(BaseEvent):
    __event_name__ = "user.created"
 
    user_id: UUID
    email: str | None
    telegram_id: int | None
 
 
@dataclass(frozen=True)
class UserRoleChangedEvent(BaseEvent):
    __event_name__ = "user.role_changed"
 
    user_id: UUID
    old_role: str
    new_role: str
 
 