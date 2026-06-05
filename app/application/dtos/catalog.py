from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.offer import Offer
from app.domain.entities.price import Price
from app.domain.entities.product import Product
from app.domain.entities.plan import Plan


@dataclass
class ProductDTO(BaseDTO):
    id: UUID
    code: str
    name: str
    product_type: str
    description: str
    is_active: bool

    @classmethod
    def from_entity(cls, entity: Product) -> Self:
        return cls(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            product_type=entity.product_type.value,
            description=entity.description,
            is_active=entity.is_active,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@dataclass
class PlanDTO(BaseDTO):
    id: UUID
    code: str
    name: str
    plan_type: str
    product_id: UUID | None
    product_type: str
    visibility: str
    description: str
    is_active: bool
    is_public: bool
    sort_order: int

    @classmethod
    def from_entity(cls, entity: Plan) -> Self:
        return cls(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            plan_type=entity.plan_type.value,
            product_id=entity.product_id,
            product_type=entity.product_type.value,
            visibility=entity.visibility.value,
            description=entity.description,
            is_active=entity.is_active,
            is_public=entity.is_public,
            sort_order=entity.sort_order,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@dataclass
class PriceDTO(BaseDTO):
    id: UUID
    plan_id: UUID
    amount: Decimal
    currency: str
    price_type: str
    billing_interval: str
    duration_days: int | None
    traffic_limit_gb: Decimal | None
    device_count: int | None
    country_code: str | None
    tax_category: str | None
    promo_eligible: bool
    active_from: date | None
    active_to: date | None
    is_active: bool

    @classmethod
    def from_entity(cls, entity: Price) -> Self:
        return cls(
            id=entity.id,
            plan_id=entity.plan_id,
            amount=entity.money.amount,
            currency=entity.money.currency,
            price_type=entity.price_type.value,
            billing_interval=entity.billing_interval.value,
            duration_days=entity.duration_days,
            traffic_limit_gb=entity.traffic_limit_gb,
            device_count=entity.device_count,
            country_code=entity.context.country_code,
            tax_category=entity.context.tax_category,
            promo_eligible=entity.context.promo_eligible,
            active_from=entity.context.active_from,
            active_to=entity.context.active_to,
            is_active=entity.is_active,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


@dataclass
class OfferDTO(BaseDTO):
    id: UUID
    plan_id: UUID
    price_id: UUID
    title: str
    subtitle: str
    marketing_labels: tuple[str, ...]
    terms: str
    status: str
    discount_percent: Decimal | None
    trial_days: int | None
    sort_order: int

    @classmethod
    def from_entity(cls, entity: Offer) -> Self:
        return cls(
            id=entity.id,
            plan_id=entity.plan_id,
            price_id=entity.price_id,
            title=entity.title,
            subtitle=entity.subtitle,
            marketing_labels=entity.marketing_labels,
            terms=entity.terms,
            status=entity.status.value,
            discount_percent=entity.discount_percent,
            trial_days=entity.trial_days,
            sort_order=entity.sort_order,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
