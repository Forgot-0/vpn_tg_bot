from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.payment import PaymentOrder


class PaymentOrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> PaymentOrder | None: ...
 
    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> PaymentOrder | None: ...
 
    @abstractmethod
    async def get_pending_for_subscription(
        self, subscription_id: UUID
    ) -> PaymentOrder | None: ...
 
    @abstractmethod
    async def add(self, payment: PaymentOrder) -> None: ...
 
    @abstractmethod
    async def update(self, payment: PaymentOrder) -> None: ...
 
