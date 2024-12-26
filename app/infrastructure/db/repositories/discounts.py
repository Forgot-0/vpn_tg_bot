from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.discount import Discount, DiscountUser
from domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository
from infrastructure.db.convertors.discounts import (
    convert_discount_dict_to_entity,
    convert_discount_entity_to_dict,
    convert_discount_user_dict_to_entity,
    convert_discount_user_entity_to_dict
)
from infrastructure.db.repositories.base import BaseMongoDBRepository


@dataclass
class MongoDiscountRepository(BaseDiscountRepository, BaseMongoDBRepository):
    async def create(self, discount: Discount) -> None:
        document = convert_discount_entity_to_dict(discount=discount)
        await self._collection.insert_one(document=document)

    async def get_by_id(self, id: UUID) -> Discount | None:
        document = await self._collection.find_one({"_id": id})
        if document: convert_discount_dict_to_entity(data=document)
    
    async def get(self) -> list[Discount]:
        documents = await self._collection.find(
            {
                'is_active': True,
            }
        ).to_list(length=None)
        if documents: return [convert_discount_dict_to_entity(document) for document in documents]

@dataclass
class MongoDiscountUserRepository(BaseDiscountUserRepository, BaseMongoDBRepository):
    async def create(self, discount_user: DiscountUser) -> None:
        document = convert_discount_user_entity_to_dict(discount_user)
        await self._collection.insert_one(document=document)

    async def get_by_discount_user(self, discount_id: UUID, user_id: UUID):
        document = await self._collection.find_one(
            {
                'user_id': user_id,
                'discount_id': discount_id,
            }
        )
        if document: convert_discount_user_dict_to_entity(document)
    
    async def incr_count(self, discount_id: UUID, user_id: UUID, incr: int = 1) -> None:
        await self._collection.update_one(
            filter={
                'user_id': user_id,
                'discount_id': discount_id,
            },
            update={
                "$inc": {
                    'count': incr
                }
            }
        )