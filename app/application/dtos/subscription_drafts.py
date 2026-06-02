from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.subscription_draft import SubscriptionDraft


@dataclass
class SubscriptionDraftDTO(BaseDTO):
    id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID | None
    status: str
    calculated_amount: Decimal | None
    calculated_currency: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: SubscriptionDraft) -> Self:
        amount = None
        currency = None
        if entity.calculated_price is not None:
            amount = entity.calculated_price.amount
            currency = entity.calculated_price.currency

        return cls(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            status=entity.status.value,
            calculated_amount=amount,
            calculated_currency=currency,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
