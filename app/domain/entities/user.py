from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.entities.subscription import Subscription
from app.domain.events.users.created import NewUserEvent
from app.domain.events.users.referred import ReferralAssignedEvent, ReferredUserEvent
from app.domain.exception.base import CanNotReferalYourselfException
from app.domain.services.utils import now_utc
from app.domain.values.users import UserId, UserRole



@dataclass
class User(AggregateRoot):
    id: UserId = field(default_factory=lambda: UserId(uuid4()), kw_only=True)
    role: UserRole = field(default=UserRole.USER)

    telegram_id: int | None = None

    is_premium: bool = field(default=False)
    username: str | None = field(default=None)
    fullname: str | None = field(default=None)
    phone: str | None = field(default=None)

    referred_by: UserId | None = field(default=None)
    referrals_count: int = field(default=0)

    created_at: datetime = field(default_factory=now_utc)

    subscriptions: list[Subscription] = field(default_factory=list)

    @classmethod
    def create(
            cls,
            telegram_id: int,
            is_premium: bool | None=False,
            username: str | None=None,
            fullname: str | None=None,
            phone: str | None=None,
            referred_by: UserId | None=None
        ) -> 'User':

        user = cls(
            telegram_id=telegram_id,
            is_premium=is_premium if is_premium else False,
            username=username,
            fullname=fullname,
            phone=phone,
            referred_by=referred_by
        )

        if referred_by:
            user.register_event(
                ReferredUserEvent(
                    referral_id=user.id.value,
                    referred_by=referred_by.value
                )
            )

        user.register_event(
            NewUserEvent(
                user_id=user.id.value,
                username=user.username
            )
        )

        return user

    def assignReferral(self, referral_id: UserId) -> None:
        if self.id == referral_id:
            raise CanNotReferalYourselfException(referral_id=self.id.as_generic_type())

        self.referrals_count += 1

        self.register_event(
            ReferralAssignedEvent(
                user_id=self.id.value,
                referral_id=referral_id.value
            )
        )