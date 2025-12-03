from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.domain.entities.payment import Payment


@dataclass
class BasePaymentService(ABC):

    @abstractmethod
    async def create(self, order: Payment) -> tuple[str, str]: ...

    @abstractmethod
    async def check(self, payment_id: UUID) -> dict[str, Any]: ...