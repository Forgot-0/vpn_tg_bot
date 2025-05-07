from typing import List, Optional
from uuid import UUID
from domain.entities.order import Order, PaymentStatus
from domain.repositories.orders import BaseOrderRepository


class MockOrderRepository(BaseOrderRepository):
    def __init__(self):
        self._data: dict[UUID, Order] = {}

    async def create(self, order: Order) -> None:
        self._data[order.id] = order

    async def pay(self, id: UUID) -> None:
        if id in self._data:
            order = self._data[id]
            order.status = PaymentStatus("SUCCESE")
            self._data[id] = order

    async def get_by_id(self, id: UUID) -> Optional[Order]:
        return self._data.get(id)

    async def get_by_payment_id(self, payment_id: UUID) -> Optional[Order]:
        for order in self._data.values():
            if order.payment_id == payment_id:
                return order
        return None

    async def get_by_user_id(self, user_id: int) -> List[Order]:
        return [order for order in self._data.values() if order.user_id == user_id]

    async def update(self, order: Order) -> None:
        self._data[order.id] = order