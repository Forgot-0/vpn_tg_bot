from __future__ import annotations

from decimal import Decimal

from app.domain.entities.subscription import Subscription
from app.domain.values.money import Money
from app.domain.values.subscriptions import (
    AccessCredential,
    AccessFormat,
    SubscriptionSpec,
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
            spec=cls._spec_from_json(model.spec),
            status=SubscriptionStatus(model.status),
            payment_order_id=model.payment_order_id,
            purchased_price=purchased_price,
            started_at=model.started_at,
            expires_at=model.expires_at,
            used_traffic_gb=Decimal(model.used_traffic_gb),
            access_credentials=cls._credentials_from_json(model.access_credentials),
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
            spec=cls._spec_to_json(entity.spec),
            status=entity.status.value,
            payment_order_id=entity.payment_order_id,
            purchased_amount=purchased_amount,
            purchased_currency=purchased_currency,
            started_at=entity.started_at,
            expires_at=entity.expires_at,
            used_traffic_gb=entity.used_traffic_gb,
            access_credentials=cls._credentials_to_json(entity.access_credentials),
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
        model.spec = cls._spec_to_json(entity.spec)
        model.status = entity.status.value
        model.payment_order_id = entity.payment_order_id
        model.purchased_amount = purchased_amount
        model.purchased_currency = purchased_currency
        model.started_at = entity.started_at
        model.expires_at = entity.expires_at
        model.used_traffic_gb = float(entity.used_traffic_gb)
        model.access_credentials = cls._credentials_to_json(entity.access_credentials)
