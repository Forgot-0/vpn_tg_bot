from __future__ import annotations

from decimal import Decimal
from typing import cast

from app.domain.entities.order import Order
from app.domain.values.money import Money
from app.domain.values.order import OrderStatus, OrderType
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import (
    Duration,
    DeviceLimit,
    RenewalMode,
    SubscriptionLimits,
    TrafficLimit,
    TrafficResetPolicy,
    TrafficResetStrategy,
)
from app.infrastructure.db.models.order import OrderModel


def _dump_subscription_limits(limit: SubscriptionLimits | None) -> dict[str, object] | None:
    if limit is None:
        return None

    return {
        "duration_days": limit.duration_days.days,
        "traffic_limit_bytes": limit.traffic_limit_gb.bytes_limit,
        "max_devices": limit.max_devices.max_devices,
        "features": sorted(item.value for item in limit.features),
        "protocols": sorted(item.value for item in limit.protocols),
        "traffic_limit_strategy": limit.traffic_limit_strategy.strategy.value,
        "reset_every_n_days": limit.traffic_limit_strategy.reset_every_n_days,
        "custom_cron": limit.traffic_limit_strategy.custom_cron,
    }


def _load_subscription_limits(raw: dict[str, object] | None) -> SubscriptionLimits | None:
    if raw is None:
        return None

    return SubscriptionLimits(
        duration_days=Duration(cast(int | None, raw.get("duration_days"))),
        traffic_limit_gb=TrafficLimit(cast(int | None, raw.get("traffic_limit_bytes"))),
        max_devices=DeviceLimit(cast(int | None, raw.get("max_devices"))),
        features={FeatureCode(value) for value in cast(list[str], raw.get("features", []))},
        protocols={ProtocolCode(value) for value in cast(list[str], raw.get("protocols", []))},
        traffic_limit_strategy=TrafficResetPolicy(
            strategy=TrafficResetStrategy(cast(str, raw.get("traffic_limit_strategy"))),
            reset_every_n_days=cast(int | None, raw.get("reset_every_n_days")),
            custom_cron=cast(str | None, raw.get("custom_cron")),
        ),
    )


class OrderMapper:
    @staticmethod
    def from_order_domain_to_model(order: Order) -> OrderModel:
        return OrderModel(
            id=order.id,
            user_id=order.user_id,
            subscription_id=order.subscription_id,
            amount=order.amount.amount,
            currency=order.amount.currency,
            type=order.type.value,
            status=order.status.value,
            subscription_limit=_dump_subscription_limits(order.subscription_limit),
            renewal_mode=order.renewal_mode.value if order.renewal_mode is not None else None,
            created_at=order.created_at,
            paid_at=order.paid_at,
            expires_at=order.expires_at,
        )

    @staticmethod
    def from_order_model_to_domain(order_model: OrderModel) -> Order:
        return Order(
            id=order_model.id,
            user_id=order_model.user_id,
            subscription_id=order_model.subscription_id,
            amount=Money(amount=Decimal(str(order_model.amount)), currency=order_model.currency),
            type=OrderType(order_model.type),
            status=OrderStatus(order_model.status),
            subscription_limit=_load_subscription_limits(order_model.subscription_limit),
            renewal_mode=RenewalMode(order_model.renewal_mode) if order_model.renewal_mode else None,
            created_at=order_model.created_at,
            paid_at=order_model.paid_at,
            expires_at=order_model.expires_at,
        )
