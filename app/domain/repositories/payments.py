from abc import abstractmethod
from uuid import UUID

from app.domain.entities.payment import PaymentOrder
from app.domain.repositories.base import Repository


class PaymentOrderRepository(Repository[PaymentOrder, UUID]):
    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> PaymentOrder | None:
        ...

    @abstractmethod
    async def get_by_subscription_id(self, subscription_id: UUID) -> PaymentOrder | None:
        ...

    @abstractmethod
    async def add(self, payment: PaymentOrder) -> None:
        ...

    @abstractmethod
    async def update(self, payment: PaymentOrder) -> None:
        ...

