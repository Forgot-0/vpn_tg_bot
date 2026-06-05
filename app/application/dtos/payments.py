from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.payment import PaymentIntent
from app.domain.values.payments import PaymentStatus


@dataclass(frozen=True)
class GatewayPaymentResult:
    external_id: str
    status: PaymentStatus
    confirmation_url: str | None
 
 
@dataclass(frozen=True)
class GatewayStatusResult:
    external_id: str
    status: PaymentStatus
    paid_at: datetime | None

