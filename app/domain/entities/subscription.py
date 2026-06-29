from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Self
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.events.subscriptions import (
    SubscriptionActivatedEvent,
    SubscriptionCancelledEvent,
    SubscriptionExpiredEvent,
    SubscriptionPendingProvisioningEvent,
    SubscriptionProvisioningFailedEvent,
    SubscriptionRenewedEvent,
    SubscriptionSuspendedEvent,
    TrafficConsumedEvent,
)
from app.domain.services.clock import now_utc
from app.domain.values.subscriptions import (
    RenewalMode,
    RenewalStrategy,
    SubscriptionLimits,
    SubscriptionStatus,
    UsageStats,
    VpnClient,
)


@dataclass
class Subscription(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    user_id: UUID

    plan_id: UUID

    limit: SubscriptionLimits
    status: SubscriptionStatus = field(default=SubscriptionStatus.PENDING_PAYMENT)

    activated_at: datetime | None = field(default=None)
    expires_at: datetime | None = field(default=None)
    current_period_start: datetime | None = field(default=None)
    current_period_end: datetime | None = field(default=None)

    usage: UsageStats = field(default_factory=UsageStats)
    vpn_client: list[VpnClient] = field(default_factory=list)
    created_at: datetime = field(default_factory=now_utc)

    def validate(self) -> None:
        pass

    @classmethod
    def create(
        cls,
        *,
        user_id: UUID,
        plan_id: UUID,
        limit: SubscriptionLimits,
    ) -> Self:
        return cls(
            user_id=user_id,
            plan_id=plan_id,
            limit=limit,
            status=SubscriptionStatus.PENDING_PAYMENT,
        )

    def pending_provisioning(self, server_id: UUID, external_id: str) -> None:
        if self.status == SubscriptionStatus.CANCELLED:
            raise

        self.status = SubscriptionStatus.PENDING_PROVISIONING
        self.vpn_client.append(
            VpnClient(server_id=server_id, provider_external_id=external_id)
        )
        self.register_event(
            SubscriptionPendingProvisioningEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                server_id=server_id,
            )
        )

    def failed_provisioning(self, server_id: UUID, reason: str) -> None:
        self.status = SubscriptionStatus.PROVISIONING_FAILED
        self.register_event(
            SubscriptionProvisioningFailedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                server_id=server_id,
                reason=reason,
            )
        )

    def activate(self) -> None:
        if self.status not in {
            SubscriptionStatus.PENDING_PAYMENT,
            SubscriptionStatus.PENDING_PROVISIONING,
        }:
            raise

        start = now_utc()
        self.status = SubscriptionStatus.ACTIVE
        self.activated_at = start
        self.current_period_start = start

        td = self.limit.duration_days.as_timedelta
        if td is not None:
            self.expires_at = start + td
            self.current_period_end = self.expires_at

        self.register_event(
            SubscriptionActivatedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                started_at=start.date(),
                expires_at=self.expires_at.date() if self.expires_at else None,
            )
        )

    def suspend(self, reason: str) -> None:
        if self.status != SubscriptionStatus.ACTIVE:
            raise

        self.status = SubscriptionStatus.SUSPENDED
        self.register_event(
            SubscriptionSuspendedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                reason=reason,
            )
        )

    def expire(self) -> None:
        self.status = SubscriptionStatus.EXPIRED
        self.register_event(
            SubscriptionExpiredEvent(subscription_id=self.id, user_id=self.user_id)
        )

    def cancel(self) -> None:
        self.status = SubscriptionStatus.CANCELLED
        self.register_event(
            SubscriptionCancelledEvent(subscription_id=self.id, user_id=self.user_id)
        )

    def renew(self, strategy: RenewalStrategy, new_limit: SubscriptionLimits) -> None:
        previous = self.expires_at

        if strategy.mode == RenewalMode.EXTEND_DURATION:
            td = new_limit.duration_days.as_timedelta
            if td is not None:
                base = max(now_utc(), self.expires_at or now_utc())
                self.expires_at = base + td
                self.current_period_end = self.expires_at

        elif strategy.mode == RenewalMode.ADD_TRAFFIC:
            self.limit = SubscriptionLimits(
                duration_days=self.limit.duration_days,
                traffic_limit_gb=self.limit.traffic_limit_gb + new_limit.traffic_limit_gb,
                max_devices=self.limit.max_devices,
                features=self.limit.features,
                protocols=self.limit.protocols,
                traffic_limit_strategy=self.limit.traffic_limit_strategy,
            )

        elif strategy.mode == RenewalMode.EXTEND_AND_ADD_TRAFFIC:
            td = new_limit.duration_days.as_timedelta
            if td is not None:
                base = max(now_utc(), self.expires_at or now_utc())
                self.expires_at = base + td
                self.current_period_end = self.expires_at
            self.limit = SubscriptionLimits(
                duration_days=self.limit.duration_days,
                traffic_limit_gb=self.limit.traffic_limit_gb + new_limit.traffic_limit_gb,
                max_devices=self.limit.max_devices,
                features=self.limit.features,
                protocols=self.limit.protocols,
                traffic_limit_strategy=self.limit.traffic_limit_strategy,
            )

        elif strategy.mode == RenewalMode.REPLACE:
            self.limit = new_limit
            td = new_limit.duration_days.as_timedelta
            if td is not None:
                self.expires_at = now_utc() + td
                self.current_period_end = self.expires_at

        if self.status in {SubscriptionStatus.EXPIRED, SubscriptionStatus.SUSPENDED}:
            self.status = SubscriptionStatus.ACTIVE

        self.register_event(
            SubscriptionRenewedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                previous_expires_at=previous.date() if previous else None,
                new_expires_at=self.expires_at.date() if self.expires_at else None,
            )
        )

    def record_traffic(self, bytes_delta: int) -> None:
        self.usage.record_traffic(bytes_delta)
        self.register_event(
            TrafficConsumedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                consumed_gb=Decimal(str(bytes_delta / 1024 ** 3)),
                total_used_gb=Decimal(str(self.usage.gb_used)),
            )
        )

    def reset_traffic(self) -> None:
        self.usage.reset_traffic()

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

    @property
    def should_be_suspended(self) -> bool:
        return self.is_expired or self.is_traffic_exhausted
