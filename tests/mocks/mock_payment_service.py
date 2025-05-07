from typing import Any
from uuid import UUID
from domain.entities.order import Order
from app.infrastructure.payments.base import BasePaymentService

class MockPaymentService(BasePaymentService):
    async def create(self, order: Order) -> tuple[str, str]:
        return ("http://dummy-confirmation.url", "dummy-payment-id")

    async def check(self, payment_id: UUID) -> dict[str, Any]:
        return {"status": "confirmed", "info": "dummy metadata", "payment_id": "dummy-payment-id"}