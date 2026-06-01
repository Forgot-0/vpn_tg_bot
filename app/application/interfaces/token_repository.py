from dataclasses import dataclass
from datetime import timedelta
from typing import Protocol


@dataclass
class TokenRepository(Protocol):

    async def add_token(self, token: str, user_id: int, expiration: timedelta) -> None:
        ...

    async def is_valid_token(self, token: str) -> int | None:
        ...

    async def invalidate_token(self, token: str) -> None:
        ...
