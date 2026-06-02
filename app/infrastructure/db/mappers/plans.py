from __future__ import annotations

from decimal import Decimal

from app.domain.entities.plan import Plan
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import PlanOptionSet, PlanType, PlanVisibility, PricingRules, ProductType, PlanConfiguration
from app.infrastructure.db.mappers._serialization import (
    dump_decimal,
    dump_enum_set,
    load_decimal,
    load_enum_set,
)
from app.infrastructure.db.mappers.subscriptions import SubscriptionMapper
from app.infrastructure.db.models.plans import PlanModel


class PlanMapper:
    @staticmethod
    def _constraints_to_json(constraints: PlanOptionSet) -> dict:
        return {
            "allowed_protocols": dump_enum_set(constraints.allowed_protocols),
            "allowed_features": dump_enum_set(constraints.allowed_features),
            "min_duration_days": constraints.min_duration_days,
            "max_duration_days": constraints.max_duration_days,
            "min_traffic_gb": dump_decimal(constraints.min_traffic_gb),
            "max_traffic_gb": dump_decimal(constraints.max_traffic_gb),
            "min_devices": constraints.min_devices,
            "max_devices": constraints.max_devices,
            "duration_required": constraints.duration_required,
            "traffic_required": constraints.traffic_required,
        }

    @staticmethod
    def _constraints_from_json(raw: dict) -> PlanOptionSet:
        return PlanOptionSet(
            allowed_protocols=load_enum_set(raw.get("allowed_protocols"), ProtocolCode),
            allowed_features=load_enum_set(raw.get("allowed_features"), FeatureCode),
            min_duration_days=raw.get("min_duration_days", 1),
            max_duration_days=raw.get("max_duration_days"),
            min_traffic_gb=load_decimal(raw.get("min_traffic_gb")),
            max_traffic_gb=load_decimal(raw.get("max_traffic_gb")),
            min_devices=raw.get("min_devices", 1),
            max_devices=raw.get("max_devices", 1),
            duration_required=raw.get("duration_required", True),
            traffic_required=raw.get("traffic_required", False),
        )

    @staticmethod
    def _pricing_rules_to_json(rules: PricingRules) -> dict:
        return {
            "currency": rules.currency,
            "base_fee": dump_decimal(rules.base_fee),
            "per_day_rate": dump_decimal(rules.per_day_rate),
            "per_gb_rate": dump_decimal(rules.per_gb_rate),
            "per_extra_device_rate": dump_decimal(rules.per_extra_device_rate),
            "per_protocol_rates": {
                key.value: dump_decimal(value)
                for key, value in rules.per_protocol_rates.items()
            },
            "per_feature_rates": {
                key.value: dump_decimal(value)
                for key, value in rules.per_feature_rates.items()
            },
            "minimum_price": dump_decimal(rules.minimum_price),
        }

    @staticmethod
    def _pricing_rules_from_json(raw: dict) -> PricingRules:
        return PricingRules(
            currency=raw.get("currency", "USD"),
            base_fee=load_decimal(raw.get("base_fee")) or Decimal("0"),
            per_day_rate=load_decimal(raw.get("per_day_rate")) or Decimal("0"),
            per_gb_rate=load_decimal(raw.get("per_gb_rate")) or Decimal("0"),
            per_extra_device_rate=load_decimal(raw.get("per_extra_device_rate")) or Decimal("0"),
            per_protocol_rates={
                ProtocolCode(key): load_decimal(value) or Decimal("0")
                for key, value in (raw.get("per_protocol_rates") or {}).items()
            },
            per_feature_rates={
                FeatureCode(key): load_decimal(value) or Decimal("0")
                for key, value in (raw.get("per_feature_rates") or {}).items()
            },
            minimum_price=load_decimal(raw.get("minimum_price")),
        )

    @classmethod
    def to_entity(cls, model: PlanModel) -> Plan:
        fixed_spec = (
            SubscriptionMapper._spec_from_json(model.fixed_spec)
            if model.fixed_spec
            else None
        )
        fixed_price = None
        if model.fixed_amount is not None and model.fixed_currency:
            fixed_price = Money(Decimal(model.fixed_amount), model.fixed_currency)

        return Plan(
            id=model.id,
            code=model.code,
            name=model.name,
            plan_type=PlanType(model.plan_type),
            product_id=getattr(model, "product_id", None),
            product_type=ProductType(getattr(model, "product_type", "vpn_subscription")),
            visibility=PlanVisibility(getattr(model, "visibility", "public")),
            fixed_spec=fixed_spec,
            fixed_price=fixed_price,
            constraints=cls._constraints_from_json(model.constraints) if model.constraints else None,
            pricing_rules=cls._pricing_rules_from_json(model.pricing_rules)
            if model.pricing_rules
            else None,
            description=model.description,
            is_active=model.is_active,
            is_public=model.is_public,
            sort_order=model.sort_order,
            allowed_region_codes=frozenset(getattr(model, "allowed_region_codes", []) or []),
            metadata=getattr(model, "meta", {}) or {},
        )

    @classmethod
    def to_model(cls, entity: Plan) -> PlanModel:
        return PlanModel(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            plan_type=entity.plan_type.value,
            product_id=entity.product_id,
            product_type=entity.product_type.value,
            visibility=entity.visibility.value,
            fixed_spec=SubscriptionMapper._spec_to_json(entity.fixed_spec)
            if entity.fixed_spec
            else None,
            fixed_amount=entity.fixed_price.amount if entity.fixed_price else None,
            fixed_currency=entity.fixed_price.currency if entity.fixed_price else None,
            constraints=cls._constraints_to_json(entity.constraints) if entity.constraints else None,
            pricing_rules=cls._pricing_rules_to_json(entity.pricing_rules)
            if entity.pricing_rules
            else None,
            description=entity.description,
            is_active=entity.is_active,
            is_public=entity.is_public,
            sort_order=entity.sort_order,
            allowed_region_codes=sorted(entity.allowed_region_codes),
            allowed_location_ids=[str(item) for item in entity.allowed_location_ids],
            allowed_server_group_ids=[str(item) for item in entity.allowed_server_group_ids],
            meta=entity.metadata,
        )

    @classmethod
    def update_model(cls, model: PlanModel, entity: Plan) -> None:
        model.code = entity.code
        model.name = entity.name
        model.plan_type = entity.plan_type.value
        model.product_id = entity.product_id
        model.product_type = entity.product_type.value
        model.visibility = entity.visibility.value
        model.fixed_spec = (
            SubscriptionMapper._spec_to_json(entity.fixed_spec) if entity.fixed_spec else None
        )
        model.fixed_amount = float(entity.fixed_price.amount) if entity.fixed_price else None
        model.fixed_currency = entity.fixed_price.currency if entity.fixed_price else None
        model.constraints = (
            cls._constraints_to_json(entity.constraints) if entity.constraints else None
        )
        model.pricing_rules = (
            cls._pricing_rules_to_json(entity.pricing_rules) if entity.pricing_rules else None
        )
        model.description = entity.description
        model.is_active = entity.is_active
        model.is_public = entity.is_public
        model.sort_order = entity.sort_order
        model.allowed_region_codes = sorted(entity.allowed_region_codes)
        model.allowed_location_ids = [str(item) for item in entity.allowed_location_ids]
        model.allowed_server_group_ids = [str(item) for item in entity.allowed_server_group_ids]
        model.meta = entity.metadata
