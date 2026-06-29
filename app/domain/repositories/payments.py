from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.payment import Payment


class PaymentRepository(ABC):

    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> Payment | None: ...

    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> Payment | None: ...

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Payment | None: ...

    @abstractmethod
    async def add(self, payment: Payment) -> None: ...

    @abstractmethod
    async def update(self, payment: Payment) -> None: ...
