from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.events.users import UserCreatedEvent, UserRoleChangedEvent
from app.domain.services.clock import now_utc
from app.domain.values.users import UserRole


@dataclass
class User(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    role: UserRole = UserRole.USER

    email: str | None = None
    password_hash: str | None = None
    telegram_id: int | None = None

    referral_code: str = field(default_factory=lambda: uuid4().hex)
    referred_by: UUID | None = None
    referrals_count: int = 0

    is_active: bool = True
    created_at: datetime = field(default_factory=now_utc)

    @classmethod
    def create(
        cls,
        *,
        email: str | None = None,
        password_hash: str | None = None,
        telegram_id: int | None = None,
        referred_by: UUID | None = None,
    ) -> Self:
        user = cls(
            email=email,
            password_hash=password_hash,
            telegram_id=telegram_id,
            referred_by=referred_by,
        )
        user.register_event(
            UserCreatedEvent(
                user_id=user.id,
                email=user.email,
                telegram_id=user.telegram_id,
            )
        )
        return user

    def change_role(self, new_role: UserRole) -> None:
        if not self.role.is_changeable:
            raise ValueError(f"Role '{self.role}' cannot be changed")
        if not new_role.is_assignable:
            raise ValueError(f"Role '{new_role}' cannot be assigned")

        old_role = self.role
        self.role = new_role
        self.register_event(
            UserRoleChangedEvent(
                user_id=self.id,
                old_role=old_role,
                new_role=new_role,
            )
        )

    def deactivate(self) -> None:
        self.is_active = False

    def increment_referrals(self) -> None:
        self.referrals_count += 1

    def _validate(self) -> None:
        if self.email is None and self.telegram_id is None:
            raise ValueError("User must have either email or telegram_id")
        if self.referred_by is not None and self.referred_by == self.id:
            raise ValueError("User cannot refer themselves")
