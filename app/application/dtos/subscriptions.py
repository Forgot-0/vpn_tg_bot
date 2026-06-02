from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.subscription import Subscription
from app.domain.entities.subscription_plan import SubscriptionPlan
from app.domain.entities.base import AggregateRoot
from app.domain.values.subscriptions import AccessCredential, AccessFormat


@dataclass
class SubscriptionPlanDTO(BaseDTO):
    id: UUID
    code: str
    name: str
    plan_type: str
    description: str
    is_active: bool
    sort_order: int

    price_amount: Decimal | None
    price_currency: str | None

    min_duration_days: int | None
    max_duration_days: int | None
    min_traffic_gb: Decimal | None
    max_traffic_gb: Decimal | None
    min_devices: int | None
    max_devices: int | None
    allowed_protocols: list[str]
    allowed_features: list[str]

    @classmethod
    def from_entity(cls, entity: SubscriptionPlan) -> Self:
        price_amount = None
        price_currency = None

        if entity.fixed_price is not None:
            price_amount = entity.fixed_price.amount
            price_currency = entity.fixed_price.currency

        min_dur = max_dur = None
        min_traf = max_traf = None
        min_dev = max_dev = None
        protocols: list[str] = []
        features: list[str] = []

        if entity.is_fixed and entity.fixed_spec:
            protocols = [p.value for p in entity.fixed_spec.protocols]
            features = [f.value for f in entity.fixed_spec.features]
            min_dur = max_dur = entity.fixed_spec.duration_days
            min_traf = max_traf = entity.fixed_spec.traffic_limit_gb
            min_dev = max_dev = entity.fixed_spec.max_devices

        elif entity.constraints:
            c = entity.constraints
            protocols = [p.value for p in c.allowed_protocols]
            features = [f.value for f in c.allowed_features]
            min_dur = c.min_duration_days
            max_dur = c.max_duration_days
            min_traf = c.min_traffic_gb
            max_traf = c.max_traffic_gb
            min_dev = c.min_devices
            max_dev = c.max_devices

        return cls(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            plan_type=entity.plan_type.value,
            description=entity.description,
            is_active=entity.is_active,
            sort_order=entity.sort_order,
            price_amount=price_amount,
            price_currency=price_currency,
            min_duration_days=min_dur,
            max_duration_days=max_dur,
            min_traffic_gb=min_traf,
            max_traffic_gb=max_traf,
            min_devices=min_dev,
            max_devices=max_dev,
            allowed_protocols=protocols,
            allowed_features=features,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@dataclass
class AccessCredentialDTO:
    format: str
    value: str
    protocol: str | None
    label: str

    @classmethod
    def from_entity(cls, cred: AccessCredential) -> Self:
        return cls(
            format=cred.format.value,
            value=cred.value,
            protocol=cred.protocol.value if cred.protocol else None,
            label=cred.label,
        )


@dataclass
class SubscriptionDTO(BaseDTO):
    id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    status: str
    started_at: date | None
    expires_at: date | None
    used_traffic_gb: Decimal
    remaining_traffic_gb: Decimal | None
    access_credentials: list[AccessCredentialDTO]

    @classmethod
    def from_entity(cls, entity: Subscription) -> Self:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            status=entity.status.value,
            started_at=entity.started_at,
            expires_at=entity.expires_at,
            used_traffic_gb=entity.used_traffic_gb,
            remaining_traffic_gb=entity.remaining_traffic_gb,
            access_credentials=[
                AccessCredentialDTO.from_entity(c) for c in entity.access_credentials
            ],
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@dataclass
class CreateSubscriptionResultDTO:
    draft_id: UUID
    payment_order_id: UUID
    confirmation_url: str
    amount: Decimal
    currency: str
