from __future__ import annotations

from decimal import Decimal

from app.domain.entities.offer import Offer
from app.domain.entities.price import Price
from app.domain.entities.product import Product
from app.domain.values.money import Money
from app.domain.values.subscriptions import BillingInterval, OfferStatus, PriceContext, PriceType, ProductType
from app.infrastructure.db.models.catalog import OfferModel, PriceModel, ProductModel


class ProductMapper:
    @staticmethod
    def to_entity(model: ProductModel) -> Product:
        return Product(
            id=model.id,
            code=model.code,
            name=model.name,
            product_type=ProductType(model.product_type),
            description=model.description,
            is_active=model.is_active,
            metadata=model.meta,
        )

    @staticmethod
    def to_model(entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            product_type=entity.product_type.value,
            description=entity.description,
            is_active=entity.is_active,
            meta=entity.metadata,
        )


class PriceMapper:
    @staticmethod
    def to_entity(model: PriceModel) -> Price:
        return Price(
            id=model.id,
            plan_id=model.plan_id,
            money=Money(Decimal(model.amount), model.currency),
            price_type=PriceType(model.price_type),
            billing_interval=BillingInterval(model.billing_interval),
            duration_days=model.duration_days,
            traffic_limit_gb=Decimal(model.traffic_limit_gb) if model.traffic_limit_gb is not None else None,
            device_count=model.device_count,
            context=PriceContext(
                country_code=model.country_code,
                tax_category=model.tax_category,
                promo_eligible=model.promo_eligible,
                active_from=model.active_from,
                active_to=model.active_to,
            ),
            is_active=model.is_active,
            metadata=model.meta,
        )

    @staticmethod
    def to_model(entity: Price) -> PriceModel:
        return PriceModel(
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
            meta=entity.metadata,
        )


class OfferMapper:
    @staticmethod
    def to_entity(model: OfferModel) -> Offer:
        return Offer(
            id=model.id,
            plan_id=model.plan_id,
            price_id=model.price_id,
            title=model.title,
            subtitle=model.subtitle,
            marketing_labels=tuple(model.marketing_labels or []),
            terms=model.terms,
            status=OfferStatus(model.status),
            discount_percent=Decimal(model.discount_percent) if model.discount_percent is not None else None,
            trial_days=model.trial_days,
            sort_order=model.sort_order,
            active_from=model.active_from,
            active_to=model.active_to,
            metadata=model.meta,
        )

    @staticmethod
    def to_model(entity: Offer) -> OfferModel:
        return OfferModel(
            id=entity.id,
            plan_id=entity.plan_id,
            price_id=entity.price_id,
            title=entity.title,
            subtitle=entity.subtitle,
            marketing_labels=list(entity.marketing_labels),
            terms=entity.terms,
            status=entity.status.value,
            discount_percent=entity.discount_percent,
            trial_days=entity.trial_days,
            sort_order=entity.sort_order,
            active_from=entity.active_from,
            active_to=entity.active_to,
            meta=entity.metadata,
        )
