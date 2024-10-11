from dataclasses import dataclass, field

from domain.entities.base import AggregateRoot


@dataclass
class User(AggregateRoot):
    tg_id: int
    tg_username: str | None
    is_premium: bool = field(default=False)
    vpn_url: str | None = field(default=None)

    @classmethod
    def create(cls, tg_id, tg_username: str=None, is_premium: bool=False) -> 'User':
        return cls(
            tg_id=tg_id,
            tg_username=tg_username,
            is_premium=is_premium,
            vpn_url=None
        )
