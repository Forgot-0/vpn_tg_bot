from dataclasses import dataclass

from domain.events.base import BaseEvent
from domain.values.users import UserId


@dataclass(frozen=True)
class ReferredUserEvent(BaseEvent):
    referral_id: UserId
    referred_by: UserId


@dataclass(frozen=True)
class ReferralAssignedEvent(BaseEvent):
    user_id: UserId
    referral_id: UserId