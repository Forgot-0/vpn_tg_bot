from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.payment import Payment
from app.domain.repositories.base import BaseRepository



@dataclass
class BasePaymentRepository(BaseRepository[Payment]):
    @abstractmethod
    async def create(self, payment: Payment)-> None: ...
 
    @abstractmethod
    async def pay(self, id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Payment | None: ...

    @abstractmethod
    async def get_by_payment_id(self, payment_id: str) -> Payment | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[Payment]: ...

    @abstractmethod
    async def update(self, payment: Payment) -> None: ...