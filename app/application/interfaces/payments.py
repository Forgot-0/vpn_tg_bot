from abc import ABC, abstractmethod

from app.application.dtos.payments import GatewayPaymentResult, GatewayStatusResult
from app.domain.entities.payment import PaymentOrder
from app.domain.values.payments import PaymentProvider


class PaymentGateway(ABC):

    @property
    @abstractmethod
    def provider(self) -> PaymentProvider: ...

    @abstractmethod
    async def create_payment(
        self,
        order: PaymentOrder,
        *,
        return_url: str,
    ) -> GatewayPaymentResult: ...

    @abstractmethod
    async def get_status(
        self,
        external_id: str,
    ) -> GatewayStatusResult: ...

    @abstractmethod
    async def cancel_payment(
        self,
        external_id: str,
    ) -> None: ...

    @abstractmethod
    async def refund_payment(
        self,
        external_id: str,
        *,
        amount_to_refund: float | None = None,
    ) -> None: ...



