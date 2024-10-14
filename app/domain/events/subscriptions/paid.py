from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class PaidSubscriptionEvent(BaseEvent):
    event_title: ClassVar[str] = 'Paid Payment'

    subscription_id: UUID
    tg_id: int
    server_id: UUID
    product: int
    amount: int
    end_time: datetime