from dataclasses import dataclass
from uuid import UUID, uuid4
import aiohttp


from app.domain.entities.payment import Payment
from app.application.services.payment import BasePaymentService, PaymentAnswer


@dataclass
class TestPaymentService(BasePaymentService):

    async def create(self, order: Payment) -> PaymentAnswer:
        payment_id = uuid4().hex
        return PaymentAnswer(url=f"https://www.youtube.com/?t={payment_id}", payment_id=payment_id)

    async def check(self, payment_id: UUID) -> dict[str, str]:
        ...