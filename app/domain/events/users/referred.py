from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class ReferredUserEvent(BaseEvent):
    referral_id: int
    referred_by: int


@dataclass(frozen=True)
class ReferralAssignedEvent(BaseEvent):
    user_id: int
    referral_id: int