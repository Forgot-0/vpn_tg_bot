from dataclasses import dataclass
from datetime import date
from decimal import Decimal
 
from app.domain.events.base import BaseEvent
 
 
@dataclass(frozen=True)
class SubscriptionActivatedEvent(BaseEvent):
    __event_name__ = "subscription.activated"
 
    subscription_id: str
    user_id: str
    plan_id: str
    started_at: date
    expires_at: date | None
 
 
@dataclass(frozen=True)
class TrafficConsumedEvent(BaseEvent):
    __event_name__ = "subscription.traffic_consumed"
 
    subscription_id: str
    user_id: str
    consumed_gb: Decimal
    total_used_gb: Decimal
 