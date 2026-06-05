from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.order import Order
from app.domain.entities.checkout import CheckoutSession


class CheckoutSessionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, checkout_id: UUID) -> CheckoutSession | None: ...

    @abstractmethod
    async def add(self, checkout: CheckoutSession) -> None: ...

    @abstractmethod
    async def update(self, checkout: CheckoutSession) -> None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[CheckoutSession]: ...


class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    async def add(self, order: Order) -> None: ...

    @abstractmethod
    async def update(self, order: Order) -> None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Order]: ...
