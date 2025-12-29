from abc import abstractmethod
from dataclasses import dataclass

from app.domain.entities.user import User
from app.domain.repositories.base import BaseRepository
from app.domain.values.users import UserId


@dataclass
class BaseUserRepository(BaseRepository[User]):

    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UserId) -> User | None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...
