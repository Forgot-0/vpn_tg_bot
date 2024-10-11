from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class NewSubscriptionEvent(BaseEvent):
    event_title: ClassVar[str] = 'Create Payment'
    subscription_id: UUID
    tg_id: int
    product: int
    amount: int
    end_time: datetime