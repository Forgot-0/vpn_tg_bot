from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.order import Order
from app.domain.values.order import OrderStatus


class OrderRepository(ABC):

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Order]: ...

    @abstractmethod
    async def list_by_status(self, status: OrderStatus) -> list[Order]: ...

    @abstractmethod
    async def add(self, order: Order) -> None: ...

    @abstractmethod
    async def update(self, order: Order) -> None: ...
