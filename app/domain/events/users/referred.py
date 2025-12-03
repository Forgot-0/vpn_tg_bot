from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import BaseEvent


@dataclass(frozen=True)
class ReferredUserEvent(BaseEvent):
    referral_id: UUID
    referred_by: UUID


@dataclass(frozen=True)
class ReferralAssignedEvent(BaseEvent):
    user_id: UUID
    referral_id: UUID