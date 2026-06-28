from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.events.subscriptions import (
    SubscriptionActivatedEvent,
    SubscriptionPendingProvisioningEvent,
    SubscriptionProvisioningFailedEvent
)
from app.domain.services.clock import now_utc
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
        if self.status == SubscriptionStatus.PENDING_PAYMENT:
            assert len(self.vpn_client) == 1

    @classmethod
    def create(
        cls, user_id: UUID, limit: SubscriptionLimits,
    ) -> Self:
        instance = cls(
            user_id=user_id,
            limit=limit,
            status=SubscriptionStatus.PENDING_PAYMENT
        )

        return instance

    def activate(self) -> None:
        if self.status != SubscriptionStatus.PENDING_PAYMENT:
            raise

        start_at = now_utc()

        self.status = SubscriptionStatus.ACTIVE
        self.register_event(
            SubscriptionActivatedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                started_at=start_at,
                expires_at=(
                    start_at+self.limit.duration_days.as_timedelta
                    if self.limit.duration_days.as_timedelta is not None
                    else None
                )
            )
        )

    def pending_provisioning(self, server_id: UUID, external_id: str) -> None:
        if self.status == SubscriptionStatus.CANCELLED:
            raise

        self.status = SubscriptionStatus.PENDING_PROVISIONING
        self.vpn_client.append(
            VpnClient(
                server_id=server_id,
                provider_external_id=external_id
            )
        )
        self.register_event(
            SubscriptionPendingProvisioningEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                server_id=server_id
            )
        )

    def failed_provisioning(self, server_id: UUID, reason: str) -> None:
        self.status = SubscriptionStatus.PROVISIONING_FAILED
        self.register_event(
            SubscriptionProvisioningFailedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                server_id=server_id,
                reason=reason
            )
        )

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return now_utc() >= self.expires_at
 
    @property
    def is_traffic_exhausted(self) -> bool:
        if self.limit.traffic_limit_gb.is_unlimited:
            return False
        if self.limit.traffic_limit_gb.bytes_limit is None:
            return False
        return self.usage.bytes_used >= self.limit.traffic_limit_gb.bytes_limit
 
    @property
    def is_device_limit_reached(self) -> bool:
        limit = self.limit.max_devices.max_devices
        if limit is None:
            return False
        return self.usage.active_devices >= limit

    
