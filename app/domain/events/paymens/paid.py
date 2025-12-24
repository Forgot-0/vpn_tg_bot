
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.events.base import BaseEvent


@dataclass(frozen=True)
class PaidPaymentEvent(BaseEvent):
    order_id: UUID
    user_id: UUID
    subscription_id: UUID
    end_time: datetime