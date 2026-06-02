from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import BusinessRuleViolationError, InvalidStateTransitionError
from app.domain.events.subscriptions import (
    SubscriptionActivatedEvent,
    SubscriptionCancelledEvent,
    SubscriptionExpiredEvent,
    SubscriptionRenewedEvent,
    SubscriptionSuspendedEvent,
    TrafficConsumedEvent,
)
from app.domain.values.money import Money
from app.domain.values.subscriptions import AccessCredential, PlanConfiguration, SubscriptionStatus


@dataclass
class Subscription(AggregateRoot):
    id: UUID
    user_id: UUID
    plan_id: UUID

    spec: PlanConfiguration

    server_id: UUID | None = None
    order_id: UUID | None = None
    payment_intent_id: UUID | None = None
    status: SubscriptionStatus = SubscriptionStatus.PENDING_PAYMENT
    purchased_price: Money | None = None

    current_period_start: date | None = None
    current_period_end: date | None = None
    started_at: date | None = None
    expires_at: date | None = None

    used_traffic_gb: Decimal = Decimal("0")
    provisioned_access_ids: list[UUID] = field(default_factory=list)

    # Deprecated  field. Technical credentials belong to ProvisionedAccess.
    access_credentials: list[AccessCredential] = field(default_factory=list)

    def validate(self) -> None:
        if not self.user_id:
            raise ValueError("Subscription must belong to a user")
        if not self.plan_id:
            raise ValueError("Subscription must reference a plan")

    @classmethod
    def pending_provisioning(
        cls,
        *,
        id: UUID,
        user_id: UUID,
        plan_id: UUID,
        spec: PlanConfiguration,
        order_id: UUID | None,
        payment_intent_id: UUID,
        purchased_price: Money,
        server_id: UUID | None = None,
    ) -> Subscription:
        return cls(
            id=id,
            user_id=user_id,
            plan_id=plan_id,
            server_id=server_id,
            spec=spec,
            order_id=order_id,
            payment_intent_id=payment_intent_id,
            purchased_price=purchased_price,
            status=SubscriptionStatus.PENDING_PROVISIONING,
        )

    def activate(
        self,
        *,
        start_date: date,
        purchased_price: Money | None = None,
        access_credentials: list[AccessCredential] | None = None,
        provisioned_access_id: UUID | None = None,
    ) -> None:
        self._require_status(
            {SubscriptionStatus.PENDING_PAYMENT, SubscriptionStatus.PENDING_PROVISIONING, SubscriptionStatus.PROVISIONING_FAILED},
            action="activate",
        )
        self.status = SubscriptionStatus.ACTIVE
        self.started_at = start_date
        self.current_period_start = start_date
        if purchased_price is not None:
            self.purchased_price = purchased_price
        if access_credentials is not None:
            self.access_credentials = access_credentials
        if provisioned_access_id is not None and provisioned_access_id not in self.provisioned_access_ids:
            self.provisioned_access_ids.append(provisioned_access_id)

        if self.spec.is_time_limited:
            assert self.spec.duration_days is not None
            self.expires_at = start_date + timedelta(days=self.spec.duration_days)
            self.current_period_end = self.expires_at

        self.register_event(
            SubscriptionActivatedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id or UUID(int=0),
                started_at=self.started_at,
                expires_at=self.expires_at,
            )
        )

    def mark_provisioning_failed(self, *, reason: str) -> None:
        self._require_status({SubscriptionStatus.PENDING_PROVISIONING}, action="mark_provisioning_failed")
        self.status = SubscriptionStatus.PROVISIONING_FAILED
        self.register_event(
            SubscriptionSuspendedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                reason=reason,
            )
        )

    def renew(self, *, renewed_at: datetime) -> None:
        self._require_status(
            {SubscriptionStatus.ACTIVE, SubscriptionStatus.EXPIRED},
            action="renew",
        )
        if not self.spec.is_time_limited:
            raise BusinessRuleViolationError(reason="Unlimited subscriptions cannot be renewed")

        assert self.spec.duration_days is not None
        previous_expires_at = self.expires_at

        base = max(
            renewed_at.date(),
            self.expires_at or renewed_at.date(),
        )
        self.expires_at = base + timedelta(days=self.spec.duration_days)
        self.current_period_end = self.expires_at
        if self.current_period_start is None:
            self.current_period_start = renewed_at.date()
        self.status = SubscriptionStatus.ACTIVE

        self.register_event(
            SubscriptionRenewedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                previous_expires_at=previous_expires_at,
                new_expires_at=self.expires_at,
            )
        )

    def consume_traffic(self, gb: Decimal) -> None:
        if gb <= 0:
            raise ValueError("Consumed traffic must be positive")
        self._require_status({SubscriptionStatus.ACTIVE}, action="consume_traffic")

        self.used_traffic_gb += gb

        self.register_event(
            TrafficConsumedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                consumed_gb=gb,
                total_used_gb=self.used_traffic_gb,
            )
        )

        if self.is_traffic_exceeded:
            self.suspend(reason="traffic_limit_reached")

    def suspend(self, *, reason: str) -> None:
        self._require_status({SubscriptionStatus.ACTIVE}, action="suspend")
        self.status = SubscriptionStatus.SUSPENDED
        self.register_event(
            SubscriptionSuspendedEvent(
                subscription_id=self.id,
                user_id=self.user_id,
                reason=reason,
            )
        )

    def unsuspend(self) -> None:
        self._require_status({SubscriptionStatus.SUSPENDED}, action="unsuspend")
        if self.is_traffic_exceeded:
            raise BusinessRuleViolationError(reason="Cannot unsuspend: traffic limit still exceeded")
        self.status = SubscriptionStatus.ACTIVE

    def expire(self) -> None:
        self._require_status(
            {SubscriptionStatus.ACTIVE, SubscriptionStatus.SUSPENDED},
            action="expire",
        )
        self.status = SubscriptionStatus.EXPIRED
        self.register_event(
            SubscriptionExpiredEvent(
                subscription_id=self.id,
                user_id=self.user_id,
            )
        )

    def cancel(self) -> None:
        if self.status in {SubscriptionStatus.EXPIRED, SubscriptionStatus.CANCELLED}:
            raise InvalidStateTransitionError(reason=f"Cannot cancel subscription in status {self.status}")
        self.status = SubscriptionStatus.CANCELLED
        self.register_event(
            SubscriptionCancelledEvent(
                subscription_id=self.id,
                user_id=self.user_id,
            )
        )

    def attach_access(self, provisioned_access_id: UUID) -> None:
        if provisioned_access_id not in self.provisioned_access_ids:
            self.provisioned_access_ids.append(provisioned_access_id)

    def rotate_credentials(self, new_credentials: list[AccessCredential]) -> None:
        self._require_status(
            {SubscriptionStatus.ACTIVE, SubscriptionStatus.SUSPENDED},
            action="rotate_credentials",
        )
        self.access_credentials = new_credentials

    @property
    def is_active(self) -> bool:
        return self.status == SubscriptionStatus.ACTIVE

    @property
    def is_terminal(self) -> bool:
        return self.status in {SubscriptionStatus.EXPIRED, SubscriptionStatus.CANCELLED}

    @property
    def is_traffic_exceeded(self) -> bool:
        if not self.spec.is_traffic_limited:
            return False
        assert self.spec.traffic_limit_gb is not None
        return self.used_traffic_gb >= self.spec.traffic_limit_gb

    @property
    def remaining_traffic_gb(self) -> Decimal | None:
        if not self.spec.is_traffic_limited:
            return None
        assert self.spec.traffic_limit_gb is not None
        return max(Decimal("0"), self.spec.traffic_limit_gb - self.used_traffic_gb)

    @property
    def traffic_usage_ratio(self) -> float | None:
        if not self.spec.is_traffic_limited:
            return None
        assert self.spec.traffic_limit_gb is not None
        if self.spec.traffic_limit_gb == 0:
            return 1.0
        return float(self.used_traffic_gb / self.spec.traffic_limit_gb)

    def days_until_expiry(self, today: date) -> int | None:
        if self.expires_at is None:
            return None
        return (self.expires_at - today).days

    def _require_status(self, allowed: set[SubscriptionStatus], *, action: str) -> None:
        if self.status not in allowed:
            raise InvalidStateTransitionError(reason=f"Cannot {action} subscription in status '{self.status}'")
