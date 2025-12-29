from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.discount import Discount, DiscountUser
from app.domain.repositories.base import BaseRepository


@dataclass
class BaseDiscountRepository(BaseRepository[Discount]):
    @abstractmethod
    async def create(self, discount: Discount) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Discount | None: ...

    @abstractmethod
    async def get(self) -> list[Discount]: ...


@dataclass
class BaseDiscountUserRepository(ABC):
    @abstractmethod
    async def create(self, discount_user: DiscountUser) -> None: ...

    @abstractmethod
    async def get_by_discount_user(self, discount_id: UUID, user_id: int) -> DiscountUser: ...

    @abstractmethod
    async def incr_count(self, discount_id: UUID, user_id: int, incr: int=1) -> None: ...