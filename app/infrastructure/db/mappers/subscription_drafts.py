from __future__ import annotations

from decimal import Decimal

from app.domain.entities.subscription_draft import SubscriptionDraft
from app.domain.values.subscriptions import (
    DraftStatus,
    SubscriptionSpec,
)
from app.domain.values.money import Money
from app.infrastructure.db.models.subscription_drafts import SubscriptionDraftModel
from app.infrastructure.db.mappers._serialization import (
    dump_decimal,
    dump_enum_set,
    load_decimal,
    load_enum_set,
)
from app.domain.values.servers import FeatureCode, ProtocolCode


class SubscriptionDraftMapper:
    @staticmethod
    def _spec_to_json(spec: SubscriptionSpec) -> dict:
        return {
            "protocols": dump_enum_set(spec.protocols),
            "duration_days": spec.duration_days,
            "traffic_limit_gb": dump_decimal(spec.traffic_limit_gb),
            "max_devices": spec.max_devices,
            "features": dump_enum_set(spec.features),
        }

    @staticmethod
    def _spec_from_json(raw: dict) -> SubscriptionSpec:
        return SubscriptionSpec(
            protocols=load_enum_set(raw.get("protocols"), ProtocolCode),
            duration_days=raw.get("duration_days"),
            traffic_limit_gb=load_decimal(raw.get("traffic_limit_gb")),
            max_devices=raw["max_devices"],
            features=load_enum_set(raw.get("features"), FeatureCode),
        )

    @classmethod
    def to_entity(cls, model: SubscriptionDraftModel) -> SubscriptionDraft:
        calculated_price = None
        if model.calculated_amount is not None and model.calculated_currency:
            calculated_price = Money(Decimal(model.calculated_amount), model.calculated_currency)

        return SubscriptionDraft(
            id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            server_id=model.server_id,
            spec=cls._spec_from_json(model.spec),
            calculated_price=calculated_price,
            status=DraftStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: SubscriptionDraft) -> SubscriptionDraftModel:
        calculated_amount = None
        calculated_currency = None
        if entity.calculated_price is not None:
            calculated_amount = float(entity.calculated_price.amount)
            calculated_currency = entity.calculated_price.currency

        return SubscriptionDraftModel(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            spec=cls._spec_to_json(entity.spec),
            calculated_amount=calculated_amount,
            calculated_currency=calculated_currency,
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def update_model(cls, model: SubscriptionDraftModel, entity: SubscriptionDraft) -> None:
        calculated_amount = None
        calculated_currency = None
        if entity.calculated_price is not None:
            calculated_amount = float(entity.calculated_price.amount)
            calculated_currency = entity.calculated_price.currency

        model.user_id = entity.user_id
        model.plan_id = entity.plan_id
        model.server_id = entity.server_id
        model.spec = cls._spec_to_json(entity.spec)
        model.calculated_amount = calculated_amount
        model.calculated_currency = calculated_currency
        model.status = entity.status.value
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
