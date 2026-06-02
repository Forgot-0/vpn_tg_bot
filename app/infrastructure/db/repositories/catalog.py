from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.offer import Offer
from app.domain.entities.price import Price
from app.domain.entities.product import Product
from app.domain.repositories.catalog import OfferRepository, PriceRepository, ProductRepository
from app.domain.values.subscriptions import OfferStatus
from app.infrastructure.db.mappers.catalog import OfferMapper, PriceMapper, ProductMapper
from app.infrastructure.db.models.catalog import OfferModel, PriceModel, ProductModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyProductRepository(SQLAlchemyRepository, ProductRepository):
    async def get_by_id(self, product_id: UUID) -> Product | None:
        model = await self.session.get(ProductModel, product_id)
        return ProductMapper.to_entity(model) if model else None

    async def get_by_code(self, code: str) -> Product | None:
        result = await self.session.execute(select(ProductModel).where(ProductModel.code == code))
        model = result.scalar_one_or_none()
        return ProductMapper.to_entity(model) if model else None

    async def add(self, product: Product) -> None:
        self.session.add(ProductMapper.to_model(product))

    async def update(self, product: Product) -> None:
        model = await self.session.get(ProductModel, product.id)
        if model is None:
            raise LookupError(f"Product {product.id} not found")
        updated = ProductMapper.to_model(product)
        for key, value in updated.__dict__.items():
            if not key.startswith("_"):
                setattr(model, key, value)


@dataclass
class SQLAlchemyPriceRepository(SQLAlchemyRepository, PriceRepository):
    async def get_by_id(self, price_id: UUID) -> Price | None:
        model = await self.session.get(PriceModel, price_id)
        return PriceMapper.to_entity(model) if model else None

    async def list_active_by_plan(self, plan_id: UUID) -> list[Price]:
        stmt = select(PriceModel).where(PriceModel.plan_id == plan_id, PriceModel.is_active.is_(True))
        result = await self.session.execute(stmt)
        return [PriceMapper.to_entity(model) for model in result.scalars().all()]

    async def add(self, price: Price) -> None:
        self.session.add(PriceMapper.to_model(price))

    async def update(self, price: Price) -> None:
        model = await self.session.get(PriceModel, price.id)
        if model is None:
            raise LookupError(f"Price {price.id} not found")
        updated = PriceMapper.to_model(price)
        for key, value in updated.__dict__.items():
            if not key.startswith("_"):
                setattr(model, key, value)


@dataclass
class SQLAlchemyOfferRepository(SQLAlchemyRepository, OfferRepository):
    async def get_by_id(self, offer_id: UUID) -> Offer | None:
        model = await self.session.get(OfferModel, offer_id)
        return OfferMapper.to_entity(model) if model else None

    async def list_active(self) -> list[Offer]:
        result = await self.session.execute(
            select(OfferModel).where(OfferModel.status == OfferStatus.ACTIVE.value)
        )
        return [OfferMapper.to_entity(model) for model in result.scalars().all()]

    async def list_by_plan(self, plan_id: UUID) -> list[Offer]:
        result = await self.session.execute(select(OfferModel).where(OfferModel.plan_id == plan_id))
        return [OfferMapper.to_entity(model) for model in result.scalars().all()]

    async def add(self, offer: Offer) -> None:
        self.session.add(OfferMapper.to_model(offer))

    async def update(self, offer: Offer) -> None:
        model = await self.session.get(OfferModel, offer.id)
        if model is None:
            raise LookupError(f"Offer {offer.id} not found")
        updated = OfferMapper.to_model(offer)
        for key, value in updated.__dict__.items():
            if not key.startswith("_"):
                setattr(model, key, value)
