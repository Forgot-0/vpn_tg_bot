from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.entities.subscription import Subscription
from domain.events.users.created import NewUserEvent
from domain.events.users.referred import ReferralAssignedEvent, ReferredUserEvent
from domain.values.users import UserId



@dataclass
class User(AggregateRoot):
    id: UserId = field(default_factory=lambda: UserId(uuid4()), kw_only=True)

    telegram_id: int | None = None

    is_premium: bool = field(default=False)
    username: str | None = field(default=None)
    fullname: str | None = field(default=None)
    phone: str | None = field(default=None)

    referred_by: UserId | None = field(default=None)
    referrals_count: int = field(default=0)

    created_at: datetime = field(default_factory=datetime.now)

    subscriptions: list[Subscription] = field(default_factory=list)

    @classmethod
    def create(
            cls,
            telegram_id: int,
            is_premium: bool=False,
            username: str | None=None,
            fullname: str | None=None,
            phone: str | None=None,
            referred_by: UserId | None=None
        ) -> 'User':

        user = cls(
            telegram_id=telegram_id,
            is_premium=is_premium,
            username=username,
            fullname=fullname,
            phone=phone,
            referred_by=referred_by
        )

        if referred_by:
            user.register_event(
                ReferredUserEvent(
                    referral_id=user.id,
                    referred_by=referred_by
                )
            )

        user.register_event(
            NewUserEvent(
                user_id=user.id,
                username=user.username
            )
        )

        return user

    def assignReferral(self, referral_id: UserId) -> None:
        if self.id == referral_id:
            raise

        self.referrals_count += 1

        self.register_event(
            ReferralAssignedEvent(
                user_id=self.id,
                referral_id=referral_id
            )
        )