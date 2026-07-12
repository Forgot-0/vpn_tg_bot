from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

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


@dataclass(frozen=True)
class ConfirmPaymentResult:
    payment_id: UUID
    order_id: UUID
    status: PaymentStatus
    subscription_id: UUID | None = None
