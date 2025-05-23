
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class PaidPaymentEvent(BaseEvent):
    event_title: ClassVar[str] = 'Paid Payment'
    order_id: UUID
    user_id: UUID
    end_time: datetime