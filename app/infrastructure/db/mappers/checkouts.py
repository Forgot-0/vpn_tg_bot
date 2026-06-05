from __future__ import annotations

from decimal import Decimal

from app.domain.entities.checkout import CheckoutSession
from app.domain.values.subscriptions import (
    CheckoutStatus,
    PlanConfiguration,
)
from app.domain.values.money import Money
from app.infrastructure.db.models.checkouts import CheckoutSessionModel
from app.infrastructure.db.mappers._serialization import (
    dump_decimal,
    dump_enum_set,
    load_decimal,
    load_enum_set,
)
from app.domain.values.servers import FeatureCode, ProtocolCode


class CheckoutSessionMapper:
    @staticmethod
    def _spec_to_json(spec: PlanConfiguration) -> dict:
        return {
            "protocols": dump_enum_set(spec.protocols),
            "duration_days": spec.duration_days,
            "traffic_limit_gb": dump_decimal(spec.traffic_limit_gb),
            "max_devices": spec.max_devices,
            "features": dump_enum_set(spec.features),
        }

    @staticmethod
    def _spec_from_json(raw: dict) -> PlanConfiguration:
        return PlanConfiguration(
            protocols=load_enum_set(raw.get("protocols"), ProtocolCode),
            duration_days=raw.get("duration_days"),
            traffic_limit_gb=load_decimal(raw.get("traffic_limit_gb")),
            max_devices=raw["max_devices"],
            features=load_enum_set(raw.get("features"), FeatureCode),
        )

    @classmethod
    def to_entity(cls, model: CheckoutSessionModel) -> CheckoutSession:
        calculated_price = None
        if model.calculated_amount is not None and model.calculated_currency:
            calculated_price = Money(Decimal(model.calculated_amount), model.calculated_currency)

        return CheckoutSession(
            id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            server_id=model.server_id,
            offer_id=getattr(model, "offer_id", None),
            price_id=getattr(model, "price_id", None),
            order_id=getattr(model, "order_id", None),
            expires_at=getattr(model, "expires_at", None),
            metadata=getattr(model, "meta", {}) or {},
            spec=cls._spec_from_json(model.spec),
            calculated_price=calculated_price,
            status=CheckoutStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: CheckoutSession) -> CheckoutSessionModel:
        calculated_amount = None
        calculated_currency = None
        if entity.calculated_price is not None:
            calculated_amount = float(entity.calculated_price.amount)
            calculated_currency = entity.calculated_price.currency

        return CheckoutSessionModel(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            offer_id=entity.offer_id,
            price_id=entity.price_id,
            order_id=entity.order_id,
            expires_at=entity.expires_at,
            meta=entity.metadata,
            spec=cls._spec_to_json(entity.spec),
            calculated_amount=calculated_amount,
            calculated_currency=calculated_currency,
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def update_model(cls, model: CheckoutSessionModel, entity: CheckoutSession) -> None:
        calculated_amount = None
        calculated_currency = None
        if entity.calculated_price is not None:
            calculated_amount = float(entity.calculated_price.amount)
            calculated_currency = entity.calculated_price.currency

        model.user_id = entity.user_id
        model.plan_id = entity.plan_id
        model.server_id = entity.server_id
        model.offer_id = entity.offer_id
        model.price_id = entity.price_id
        model.order_id = entity.order_id
        model.expires_at = entity.expires_at
        model.meta = entity.metadata
        model.spec = cls._spec_to_json(entity.spec)
        model.calculated_amount = calculated_amount
        model.calculated_currency = calculated_currency
        model.status = entity.status.value
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
