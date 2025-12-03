from typing import List, Optional
from uuid import UUID
from app.domain.entities.payment import Payment, PaymentStatus
from app.domain.repositories.payment import BasePaymentRepository


class MockPaymentRepository(BasePaymentRepository):
    def __init__(self):
        self._data: dict[UUID, Payment] = {}

    async def create(self, payment: Payment) -> None:
        self._data[payment.id] = payment

    async def pay(self, id: UUID) -> None:
        if id in self._data:
            payment = self._data[id]
            payment.status = PaymentStatus("SUCCESE")
            self._data[id] = payment

    async def get_by_id(self, id: UUID) -> Optional[Payment]:
        return self._data.get(id)

    async def get_by_payment_id(self, payment_id: UUID) -> Optional[Payment]:
        for payment in self._data.values():
            if payment.payment_id == payment_id:
                return payment
        return None

    async def get_by_user_id(self, user_id: int) -> List[Payment]:
        return [payment for payment in self._data.values() if payment.user_id == user_id]

    async def update(self, payment: Payment) -> None:
        self._data[payment.id] = payment