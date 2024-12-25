from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.discount import Discount, DiscountUser


@dataclass
class BaseDiscountRepository(ABC):
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