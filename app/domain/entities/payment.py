
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.payments import PaymentProvider, PaymentStatus
from app.domain.values.subscriptions import Money


@dataclass
class PaymentOrder(AggregateRoot):
    id: UUID
    subscription_id: UUID
    price: Money
    provider: PaymentProvider

    status: PaymentStatus = PaymentStatus.PENDING

    external_payment_id: str | None = None
    confirmation_url: str | None = None
    created_at: datetime | None = None
    paid_at: datetime | None = None

