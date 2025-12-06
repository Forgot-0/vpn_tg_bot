from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.domain.entities.payment import Payment



@dataclass(frozen=True)
class PaymentAnswer:
    url: str
    payment_id: str


@dataclass
class BasePaymentService(ABC):

    @abstractmethod
    async def create(self, order: Payment) -> PaymentAnswer: ...

    @abstractmethod
    async def check(self, payment_id: UUID) -> dict[str, Any]: ...
