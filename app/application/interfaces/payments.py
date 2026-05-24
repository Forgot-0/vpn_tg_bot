from abc import abstractmethod
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from app.application.dtos.payments import CreatePaymentResult, PaymentStatusResult



class PaymentGateway(Protocol):
    @abstractmethod
    async def create_payment(
        self,
        subscription_id: UUID,
        amount: Decimal,
        currency: str,
        description: str
    ) -> CreatePaymentResult: ...

    @abstractmethod
    async def get_payment_status(self, provider_payment_id: str) -> PaymentStatusResult: ...

