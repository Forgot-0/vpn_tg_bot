from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities.order import Order


@dataclass
class BasePaymentService(ABC):

    @abstractmethod
    async def create(self, order: Order) -> tuple[str, str]: ...

    @abstractmethod
    async def check(self, payment_id: UUID) -> dict[str, Any]: ...