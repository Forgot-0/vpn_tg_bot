from __future__ import annotations

from typing import cast

from app.domain.entities.subscription import Subscription
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import (
    Duration,
    DeviceLimit,
    SubscriptionLimits,
    SubscriptionStatus,
    TrafficLimit,
    TrafficResetPolicy,
    TrafficResetStrategy,
    UsageStats,
)
from app.infrastructure.db.models.subscription import SubscriptionModel


def _dump_enum_values(values: set[FeatureCode] | set[ProtocolCode] | set[str]) -> list[str]:
    return sorted(item if isinstance(item, str) else item.value for item in values)


def _load_feature_codes(raw: list[str] | None) -> set[FeatureCode]:
    if not raw:
        return set()
    return {FeatureCode(value) for value in raw}


def _load_protocol_codes(raw: list[str] | None) -> set[ProtocolCode]:
    if not raw:
        return set()
    return {ProtocolCode(value) for value in raw}


def _dump_subscription_limits(limit: SubscriptionLimits) -> dict[str, object]:
    return {
        "duration_days": limit.duration_days.days,
        "traffic_limit_bytes": limit.traffic_limit_gb.bytes_limit,
        "max_devices": limit.max_devices.max_devices,
        "features": _dump_enum_values(limit.features),
        "protocols": _dump_enum_values(limit.protocols),
        "traffic_limit_strategy": limit.traffic_limit_strategy.strategy.value,
        "reset_every_n_days": limit.traffic_limit_strategy.reset_every_n_days,
        "custom_cron": limit.traffic_limit_strategy.custom_cron,
    }


def _load_subscription_limits(raw: dict[str, object] | None) -> SubscriptionLimits:
    assert raw is not None
    return SubscriptionLimits(
        duration_days=Duration(cast(int | None, raw.get("duration_days"))),
        traffic_limit_gb=TrafficLimit(cast(int | None, raw.get("traffic_limit_bytes"))),
        max_devices=DeviceLimit(cast(int | None, raw.get("max_devices"))),
        features=_load_feature_codes(cast(list[str] | None, raw.get("features"))),
        protocols=_load_protocol_codes(cast(list[str] | None, raw.get("protocols"))),
        traffic_limit_strategy=TrafficResetPolicy(
            strategy=TrafficResetStrategy(cast(str, raw.get("traffic_limit_strategy"))),
            reset_every_n_days=cast(int | None, raw.get("reset_every_n_days")),
            custom_cron=cast(str | None, raw.get("custom_cron")),
        ),
    )


class SubscriptionMapper:
    @staticmethod
    def from_subscription_domain_to_model(subscription: Subscription) -> SubscriptionModel:
        return SubscriptionModel(
            id=subscription.id,
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            status=subscription.status.value,
            limit=_dump_subscription_limits(subscription.limit),
            activated_at=subscription.activated_at,
            expires_at=subscription.expires_at,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            bytes_used=subscription.usage.bytes_used,
            active_devices=subscription.usage.active_devices,
            last_reset_at=subscription.usage.last_reset_at,
            server_id=subscription.server_id,
            provider_external_id=subscription.provider_external_id,
            created_at=subscription.created_at,
        )

    @staticmethod
    def from_subscription_model_to_domain(subscription_model: SubscriptionModel) -> Subscription:
        return Subscription(
            id=subscription_model.id,
            user_id=subscription_model.user_id,
            plan_id=subscription_model.plan_id,
            status=SubscriptionStatus(subscription_model.status),
            limit=_load_subscription_limits(subscription_model.limit),
            activated_at=subscription_model.activated_at,
            expires_at=subscription_model.expires_at,
            current_period_start=subscription_model.current_period_start,
            current_period_end=subscription_model.current_period_end,
            server_id=subscription_model.server_id,
            provider_external_id=subscription_model.provider_external_id,
            usage=UsageStats(
                bytes_used=subscription_model.bytes_used,
                active_devices=subscription_model.active_devices,
                last_reset_at=subscription_model.last_reset_at,
            ),
            created_at=subscription_model.created_at,
        )
