from dataclasses import dataclass, field

from domain.entities.base import AggregateRoot
from domain.events.users.created import NewUserEvent
from domain.events.users.referred import ReferredUserEvent



@dataclass
class User(AggregateRoot):
    id: int
    is_premium: bool = field(default=False)
    username: str | None = field(default=None)
    fullname: str | None = field(default=None)
    phone: str | None = field(default=None)

    referred_by: int | None = field(default=None)
    referrals_count: int = field(default=0)

    @classmethod
    def create(
            cls, 
            id: int,
            is_premium: bool,
            username: str | None=None,
            fullname: str | None=None,
            phone: str | None=None,
            referred_by: int | None=None
        ) -> 'User':

        user = cls(
            id=id,
            is_premium=is_premium,
            username=username,
            fullname=fullname,
            phone=phone,
            referred_by=referred_by
        )

        if referred_by:
            user.register_event(
                ReferredUserEvent(
                    reffered_by=referred_by
                )
            )

        return user
