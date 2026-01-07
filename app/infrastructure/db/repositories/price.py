from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from app.domain.entities.price import PriceConfig
from app.domain.repositories.price import BasePriceRepository
from app.domain.values.servers import ProtocolType, Region
from app.infrastructure.db.convertors.price import (
    convert_price_document_to_entity,
    convert_price_entity_to_document
)
from app.infrastructure.db.repositories.base import BaseMongoDBRepository


@dataclass
class PriceRepository(BaseMongoDBRepository, BasePriceRepository):
    cfg: PriceConfig

    @classmethod
    async def create(
        cls,
        cfg: PriceConfig,
        mongo_db_client: AsyncIOMotorClient,
        mongo_db_db_name: str,
        mongo_db_collection_name: str
    ) -> "PriceRepository":
        instance = cls(
            cfg=cfg,
            mongo_db_client=mongo_db_client,
            mongo_db_db_name=mongo_db_db_name,
            mongo_db_collection_name=mongo_db_collection_name,
        )
        try:
            await instance._collection.insert_one(
                convert_price_entity_to_document(cfg)
            )
        except DuplicateKeyError:
            data = await instance._collection.find_one({"_id": 1})
            if data is None:
                raise

            instance.cfg = convert_price_document_to_entity(
                data
            )

        return instance

    async def get_price_config(self) -> PriceConfig:
        return self.cfg

    async def add_region(self, region: Region, coef: float) -> None:
        if region in self.cfg.region_multipliers:
            raise

        self.cfg.region_multipliers[region] = coef
        await self.update(self.cfg)

    async def add_protocol(self, protocol: ProtocolType, coef: float) -> None:
        if protocol in self.cfg.protocol_multipliers:
            raise

        self.cfg.protocol_multipliers[protocol] = coef
        await self.update(self.cfg)

    async def update(self, cfg: PriceConfig) -> None:
        self.cfg = cfg
        await self._collection.update_one(
            {"_id": 1}, update=convert_price_entity_to_document(cfg)
        )
