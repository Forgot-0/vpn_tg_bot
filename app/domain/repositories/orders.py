from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.order import Order



@dataclass
class BaseOrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order)-> None: ...
 
    @abstractmethod
    async def pay(self, id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Order | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[Order]: ...

    @abstractmethod
    async def update(self, order: Order) -> None: ...