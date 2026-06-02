from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from app.domain.entities.subscription import Subscription
from app.domain.values.money import Money
from app.domain.values.subscriptions import (
    AccessCredential,
    AccessFormat,
    PlanConfiguration,
    SubscriptionStatus,
)
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.infrastructure.db.mappers._serialization import (
    dump_decimal,
    dump_enum_set,
    load_decimal,
    load_enum_set,
)
from app.infrastructure.db.models.subscriptions import SubscriptionModel


class SubscriptionMapper:
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

    @staticmethod
    def _credentials_to_json(credentials: list[AccessCredential]) -> list[dict]:
        return [
            {
                "format": item.format.value,
                "value": item.value,
                "protocol": item.protocol.value if item.protocol else None,
                "panel_client_id": item.panel_client_id,
                "label": item.label,
            }
            for item in credentials
        ]

    @staticmethod
    def _credentials_from_json(raw: list[dict] | None) -> list[AccessCredential]:
        if not raw:
            return []
        result: list[AccessCredential] = []
        for item in raw:
            protocol_raw = item.get("protocol")
            result.append(
                AccessCredential(
                    format=AccessFormat(item["format"]),
                    value=item["value"],
                    protocol=ProtocolCode(protocol_raw) if protocol_raw else None,
                    panel_client_id=item.get("panel_client_id"),
                    label=item.get("label", ""),
                )
            )
        return result

    @classmethod
    def to_entity(cls, model: SubscriptionModel) -> Subscription:
        purchased_price = None
        if model.purchased_amount is not None and model.purchased_currency:
            purchased_price = Money(Decimal(model.purchased_amount), model.purchased_currency)

        return Subscription(
            id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            server_id=model.server_id,
            order_id=getattr(model, "order_id", None),
            spec=cls._spec_from_json(model.spec),
            status=SubscriptionStatus(model.status),
            payment_intent_id=model.payment_intent_id,
            purchased_price=purchased_price,
            started_at=model.started_at,
            expires_at=model.expires_at,
            current_period_start=getattr(model, "current_period_start", None) or model.started_at,
            current_period_end=getattr(model, "current_period_end", None) or model.expires_at,
            used_traffic_gb=Decimal(model.used_traffic_gb),
            access_credentials=cls._credentials_from_json(model.access_credentials),
            provisioned_access_ids=[UUID(item) for item in (getattr(model, "provisioned_access_ids", []) or [])],
        )

    @classmethod
    def to_model(cls, entity: Subscription) -> SubscriptionModel:
        purchased_amount = None
        purchased_currency = None
        if entity.purchased_price is not None:
            purchased_amount = entity.purchased_price.amount
            purchased_currency = entity.purchased_price.currency

        return SubscriptionModel(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            order_id=entity.order_id,
            spec=cls._spec_to_json(entity.spec),
            status=entity.status.value,
            payment_intent_id=entity.payment_intent_id,
            purchased_amount=purchased_amount,
            purchased_currency=purchased_currency,
            started_at=entity.started_at,
            expires_at=entity.expires_at,
            current_period_start=entity.current_period_start,
            current_period_end=entity.current_period_end,
            used_traffic_gb=entity.used_traffic_gb,
            access_credentials=cls._credentials_to_json(entity.access_credentials),
            provisioned_access_ids=[str(item) for item in entity.provisioned_access_ids],
        )

    @classmethod
    def update_model(cls, model: SubscriptionModel, entity: Subscription) -> None:
        purchased_amount = None
        purchased_currency = None
        if entity.purchased_price is not None:
            purchased_amount = float(entity.purchased_price.amount)
            purchased_currency = entity.purchased_price.currency

        model.user_id = entity.user_id
        model.plan_id = entity.plan_id
        model.server_id = entity.server_id
        model.order_id = entity.order_id
        model.spec = cls._spec_to_json(entity.spec)
        model.status = entity.status.value
        model.payment_intent_id = entity.payment_intent_id
        model.purchased_amount = purchased_amount
        model.purchased_currency = purchased_currency
        model.started_at = entity.started_at
        model.expires_at = entity.expires_at
        model.current_period_start = entity.current_period_start
        model.current_period_end = entity.current_period_end
        model.used_traffic_gb = float(entity.used_traffic_gb)
        model.access_credentials = cls._credentials_to_json(entity.access_credentials)
        model.provisioned_access_ids = [str(item) for item in entity.provisioned_access_ids]
