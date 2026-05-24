from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.payment import PaymentOrder


@dataclass
class PaymentOrderDTO(BaseDTO):
    id: UUID
    subscription_id: UUID
    price_amount: Decimal
    price_currency: str
    provider: str
    status: str
    external_payment_id: str | None
    confirmation_url: str | None
    created_at: datetime | None
    paid_at: datetime | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)

    @classmethod
    def from_entity(cls, entity: PaymentOrder) -> Self:
        return cls(
            id=entity.id,
            subscription_id=entity.subscription_id,
            price_amount=entity.price.amount,
            price_currency=entity.price.currency,
            provider=entity.provider.value,
            status=entity.status.value,
            external_payment_id=entity.external_payment_id,
            confirmation_url=entity.confirmation_url,
            created_at=entity.created_at,
            paid_at=entity.paid_at,
        )
