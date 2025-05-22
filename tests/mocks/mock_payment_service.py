from typing import Any
from uuid import UUID
from domain.entities.payment import Payment
from app.infrastructure.payments.base import BasePaymentService

class MockPaymentService(BasePaymentService):
    async def create(self, order: Payment) -> tuple[str, str]:
        return ("http://dummy-confirmation.url", "c92aa23f-d451-4404-9c11-71a4558e903f")

    async def check(self, payment_id: UUID) -> dict[str, Any]:
        return {"status": "confirmed", "info": "dummy metadata", "payment_id": "dummy-payment-id"}