from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.domain.entities.payment import Payment


@dataclass
class PaymentDTO(BaseDTO):
    id: UUID
    subscription: SubscriptionDTO
    user_id: UUID
    total_price: float
    status: str

    payment_id: str | None
    payment_date: datetime | None
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Payment) -> 'PaymentDTO':
        return PaymentDTO(
            id=entity.id,
            subscription=SubscriptionDTO.from_entity(entity.subscription),
            user_id=entity.user_id.value,
            total_price=entity.total_price,
            status=entity.status.value,
            payment_id=entity.payment_id,
            payment_date=entity.payment_date,
            created_at=entity.created_at
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Any:
        ...