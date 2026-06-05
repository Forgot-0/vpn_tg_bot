from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.payment import PaymentIntent


class PaymentIntentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> PaymentIntent | None: ...
 
    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> PaymentIntent | None: ...
 
    @abstractmethod
    async def get_pending_for_checkout(
        self, checkout_session_id: UUID
    ) -> PaymentIntent | None: ...
 
    @abstractmethod
    async def add(self, payment: PaymentIntent) -> None: ...
 
    @abstractmethod
    async def update(self, payment: PaymentIntent) -> None: ...
 
