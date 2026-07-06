from __future__ import annotations

from decimal import Decimal
from typing import cast

from app.domain.entities.plan import PricingRule, SubscriptionPlan
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import (
    Duration,
    DeviceLimit,
    PlanVisibility,
    SubscriptionLimits,
    TrafficLimit,
    TrafficResetPolicy,
    TrafficResetStrategy,
)
from app.infrastructure.db.mappers._serialization import (
    dump_money,
    dump_money_list,
    load_money,
    load_money_set,
)
from app.infrastructure.db.models.plan import SubscriptionPlanModel


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


def _load_subscription_limits(raw: dict[str, object] | None) -> SubscriptionLimits | None:
    if raw is None:
        return None

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


class PlanMapper:
    @staticmethod
    def from_plan_domain_to_model(plan: SubscriptionPlan) -> SubscriptionPlanModel:
        return SubscriptionPlanModel(
            id=plan.id,
            code=plan.code,
            name=plan.name,
            description=plan.description,
            duration_days=plan.limit.duration_days.days if plan.limit else None,
            traffic_limit_bytes=plan.limit.traffic_limit_gb.bytes_limit if plan.limit else None,
            max_devices=plan.limit.max_devices.max_devices if plan.limit else None,
            features=_dump_enum_values(plan.limit.features if plan.limit is not None else set()),
            protocols=_dump_enum_values(plan.limit.protocols if plan.limit is not None else set()),
            strategy=(
                plan.limit.traffic_limit_strategy.strategy
                if plan.limit is not None
                else TrafficResetStrategy.NO_RESET
            ),
            reset_every_n_days=(
                plan.limit.traffic_limit_strategy.reset_every_n_days
                if plan.limit is not None
                else None
            ),
            custom_cron=(
                plan.limit.traffic_limit_strategy.custom_cron
                if plan.limit is not None
                else None
            ),
            price=dump_money_list(plan.price),
            price_rule=_dump_price_rule(plan.price_rule),
            visibility=plan.visibility,
            order_index=plan.order_index,
            is_trial=plan.is_trial,
            is_active=plan.is_active,
            allowed_durations=sorted(plan.allowed_durations),
            allowed_traffic_gb=[Decimal(str(value)) for value in sorted(plan.allowed_traffic_gb)],
            max_devices_limit=plan.max_devices_limit,
            allowed_features=_dump_enum_values(plan.allowed_features),
            allowed_protocols=_dump_enum_values(plan.allowed_protocols),
            server_id=plan.server_id,
        )

    @staticmethod
    def from_plan_model_to_domain(plan_model: SubscriptionPlanModel) -> SubscriptionPlan:
        return SubscriptionPlan(
            id=plan_model.id,
            code=plan_model.code,
            name=plan_model.name,
            description=plan_model.description,
            limit=_load_subscription_limits({
                "duration_days": plan_model.duration_days,
                "traffic_limit_bytes": plan_model.traffic_limit_bytes,
                "max_devices": plan_model.max_devices,
                "features": plan_model.features,
                "protocols": plan_model.protocols,
                "traffic_limit_strategy": plan_model.strategy.value,
                "reset_every_n_days": plan_model.reset_every_n_days,
                "custom_cron": plan_model.custom_cron,
            }) if plan_model.duration_days is not None or plan_model.traffic_limit_bytes is not None or plan_model.max_devices is not None else None,
            price=load_money_set(plan_model.price),
            price_rule=_load_price_rule(plan_model.price_rule),
            visibility=plan_model.visibility,
            order_index=plan_model.order_index,
            is_trial=plan_model.is_trial,
            is_active=plan_model.is_active,
            allowed_durations=set(plan_model.allowed_durations or []),
            allowed_traffic_gb={float(str(value)) for value in plan_model.allowed_traffic_gb or []},
            max_devices_limit=plan_model.max_devices_limit,
            allowed_features=_load_feature_codes(plan_model.allowed_features),
            allowed_protocols=_load_protocol_codes(plan_model.allowed_protocols),
            server_id=plan_model.server_id,
        )


def _dump_price_rule(rule: PricingRule | None) -> dict[str, object] | None:
    if rule is None:
        return None

    return {
        "price_per_day": dump_money(rule.price_per_day),
        "price_per_gb": dump_money(rule.price_per_gb),
        "price_per_device": dump_money(rule.price_per_device),
        "feature_surcharges": {
            item.value: dump_money(amount) for item, amount in rule.feature_surcharges.items()
        },
        "protocol_surcharges": {
            item.value: dump_money(amount) for item, amount in rule.protocol_surcharges.items()
        },
    }


def _load_money(raw: dict[str, str] | None) -> Money:
    money = load_money(raw)
    assert money is not None
    return money


def _load_price_rule(raw: dict[str, object] | None) -> PricingRule | None:
    if raw is None:
        return None

    return PricingRule(
        price_per_day=_load_money(cast(dict[str, str] | None, raw.get("price_per_day"))),
        price_per_gb=_load_money(cast(dict[str, str] | None, raw.get("price_per_gb"))),
        price_per_device=_load_money(cast(dict[str, str] | None, raw.get("price_per_device"))),
        feature_surcharges={
            FeatureCode(code): _load_money(cast(dict[str, str] | None, value))
            for code, value in cast(dict[str, dict[str, str]], raw.get("feature_surcharges", {})).items()
        },
        protocol_surcharges={
            ProtocolCode(code): _load_money(cast(dict[str, str] | None, value))
            for code, value in cast(dict[str, dict[str, str]], raw.get("protocol_surcharges", {})).items()
        },
    )
