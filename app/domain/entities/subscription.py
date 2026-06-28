from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.values.subscriptions import SubscriptionLimits, SubscriptionStatus, UsageStats, VpnClient



@dataclass
class Subscription(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    user_id: UUID

    limit: SubscriptionLimits
    status: SubscriptionStatus = field(default=SubscriptionStatus.PENDING_PAYMENT)

    activated_at: datetime | None = field(default=None)
    expires_at: datetime | None = field(default=None)

    usage: UsageStats = field(default_factory=UsageStats)
    vpn_client: list[VpnClient] = field(default_factory=list)

    def validate(self) -> None:
        ...

