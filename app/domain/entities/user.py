from dataclasses import dataclass, field

from domain.entities.base import AggregateRoot
from domain.events.users.created import NewUserEvent



@dataclass
class User(AggregateRoot):
    id: int
    is_premium: bool = field(default=False)
    username: str | None = field(default=None)
    fullname: str | None = field(default=None)
    phone: str | None = field(default=None)

    @classmethod
    def create(
            cls, 
            id: int,
            is_premium: bool,
            username: str | None=None,
            fullname: str | None=None,
            phone: str | None=None
        ) -> 'User':

        user = cls(
            id=id,
            is_premium=is_premium,
            username=username,
            fullname=fullname,
            phone=phone
        )

        # user.register_event(
        #     event=NewUserEvent(
        #         id=user.id,
        #         username=user.username
        #     )
        # )
        return user
