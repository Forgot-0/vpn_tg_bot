from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities.subscription import Subscription


@dataclass
class BasePaymentService(ABC):

    @abstractmethod
    async def create(self, subscription: Subscription) -> tuple[str, str]:
        ...
    
    @abstractmethod
    async def check(self, payment_id: UUID) -> dict[str, Any]:
        ...