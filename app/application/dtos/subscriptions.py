from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.subscription import Subscription, SubscriptionPlan


@dataclass
class SubscriptionPlanDTO(BaseDTO):
    id: UUID
    code: str
    name: str
    billing_mode: str
    duration_days: int | None
    traffic_quota_gb: int | None
    max_devices: int | None
    allowed_protocols: list[str]
    included_features: list[dict]
    fixed_price_amount: Decimal | None
    fixed_price_currency: str
    is_active: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)

    @classmethod
    def from_entity(cls, entity: SubscriptionPlan) -> Self:
        return cls(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            billing_mode=entity.billing_mode.value,
            duration_days=entity.duration.value if entity.duration else None,
            traffic_quota_gb=entity.traffic_quota.value if entity.traffic_quota else None,
            max_devices=entity.max_devices.value if entity.max_devices else None,
            allowed_protocols=[p.value for p in entity.allowed_protocols],
            included_features=[
                {"code": f.code.value, "quantity": str(f.quantity)}
                for f in entity.included_features
            ],
            fixed_price_amount=entity.fixed_price.amount if entity.fixed_price else None,
            fixed_price_currency=entity.fixed_price.currency if entity.fixed_price else "USD",
            is_active=True,
        )


@dataclass
class AccessArtifactDTO:
    format: str
    value: str
    external_id: str | None


@dataclass
class SubscriptionDTO(BaseDTO):
    id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    payment_order_id: UUID | None
    protocols: list[str]
    devices: int
    status: str
    started_at: date | None
    expires_at: date | None
    purchased_price_amount: Decimal | None
    purchased_price_currency: str
    used_traffic_gb: Decimal
    access_items: list[AccessArtifactDTO]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)

    @classmethod
    def from_entity(cls, entity: Subscription) -> Self:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            payment_order_id=entity.payment_order_id,
            protocols=[p.value for p in entity.protocols],
            devices=entity.devices.value,
            status=entity.status.value,
            started_at=entity.started_at,
            expires_at=entity.expires_at,
            purchased_price_amount=entity.purchased_price.amount if entity.purchased_price else None,
            purchased_price_currency=entity.purchased_price.currency if entity.purchased_price else "USD",
            used_traffic_gb=entity.used_traffic_gb,
            access_items=[
                AccessArtifactDTO(
                    format=a.format.value,
                    value=a.value,
                    external_id=a.external_id,
                )
                for a in entity.access_items
            ],
        )