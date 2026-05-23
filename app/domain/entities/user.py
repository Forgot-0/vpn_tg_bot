from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.events.users import NewUserEvent
from app.domain.services.utils import now_utc
from app.domain.values.users import UserRole


@dataclass
class User(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    role: UserRole = field(default=UserRole.USER)

    email: str | None = field(default=None)
    password_hash: str | None = field(default=None)

    telegram_id: int | None = field(default=None)

    referral_code: str = field(default_factory=lambda: uuid4().hex)
    referred_by: UUID | None = field(default=None)
    referrals_count: int = field(default=0)

    created_at: datetime = field(default_factory=now_utc)

    @classmethod
    def create(
        cls,
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
            NewUserEvent(
                user_id=user.id,
                email=user.email,
                telegram_id=user.telegram_id,
            )
        )
        return user

    def validate(self) -> None:
        if self.email is None and self.telegram_id is None:
            raise ValueError("User must have either email or telegram_id")
        if self.referred_by is not None and self.referred_by == self.id:
            raise ValueError("User cannot refer themselves")
