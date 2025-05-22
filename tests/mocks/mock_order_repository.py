from typing import List, Optional
from uuid import UUID
from domain.entities.payment import Payment, PaymentStatus
from domain.repositories.payment import BaseOrderRepository


class MockOrderRepository(BaseOrderRepository):
    def __init__(self):
        self._data: dict[UUID, Payment] = {}

    async def create(self, order: Payment) -> None:
        self._data[order.id] = order

    async def pay(self, id: UUID) -> None:
        if id in self._data:
            order = self._data[id]
            order.status = PaymentStatus("SUCCESE")
            self._data[id] = order

    async def get_by_id(self, id: UUID) -> Optional[Payment]:
        return self._data.get(id)

    async def get_by_payment_id(self, payment_id: UUID) -> Optional[Payment]:
        for order in self._data.values():
            if order.payment_id == payment_id:
                return order
        return None

    async def get_by_user_id(self, user_id: int) -> List[Payment]:
        return [order for order in self._data.values() if order.user_id == user_id]

    async def update(self, order: Payment) -> None:
        self._data[order.id] = order