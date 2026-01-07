from dataclasses import dataclass

from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.entities.price import PriceConfig
from app.domain.repositories.price import BasePriceRepository


@dataclass(frozen=True)
class GetPriceConfigQuery(BaseQuery):
    ...


@dataclass(frozen=True)
class GetPriceConfigQueryHandler(BaseQueryHandler[GetPriceConfigQuery, PriceConfig]):
    price_repository: BasePriceRepository

    async def handle(self, query: GetPriceConfigQuery) -> PriceConfig:
        cfg = await self.price_repository.get_price_config()
        return cfg