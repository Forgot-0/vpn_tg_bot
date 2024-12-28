from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...