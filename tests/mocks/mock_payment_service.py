from typing import Any
from uuid import UUID
from app.domain.entities.payment import Payment
from app.app.infrastructure.payments.base import BasePaymentService

class MockPaymentService(BasePaymentService):
    async def create(self, order: Payment) -> tuple[str, str]:
        return ("http://dummy.url", "11111111-1111-1111-1111-111111111111")

    async def check(self, payment_id: UUID) -> dict[str, Any]:
        return {"status": "confirmed", "info": "dummy metadata", "payment_id": "dummy-payment-id"}