from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.application.dtos.base import PaginatedResult
from app.application.dtos.users.base import UserListParams
from app.domain.entities.user import User
from app.domain.values.users import UserId


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UserId) -> User | None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...

    @abstractmethod
    async def get_list(self, filter_params: UserListParams) -> PaginatedResult[User]: ...
