from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User
from domain.values.users import UserId


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UserId) -> User | None: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...