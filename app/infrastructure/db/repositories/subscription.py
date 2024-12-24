from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.entities.subscription import Subscription
from domain.repositories.subscriptions import BaseSubscriptionRepository
from infrastructure.db.convertors.subscriptions import (
    convert_subscription_dict_to_entity,
    convert_subscription_entity_to_dict
)
from infrastructure.db.repositories.base import BaseMongoDBRepository


@dataclass
class MongoSubscriptionRepository(BaseSubscriptionRepository, BaseMongoDBRepository):
    async def create(self, subscription: Subscription) -> None:
        await self._collection.insert_one(convert_subscription_entity_to_dict(subscription))

    async def deactivate(self, id: UUID) -> None:
        await self._collection.update_one(
            {"_id": id},
            {"$set": {"is_active": False}},
        )

    async def activate(self, id: UUID) -> None:
        await self._collection.update_one(
            {"_id": id},
            {"$set": {"is_active": True}},
        )

    async def get(self) -> list[Subscription]:
        documents = await self._collection.find({'is_active': True}).to_list(length=None)
        if documents: return [convert_subscription_dict_to_entity(document) for document in documents]

    async def get_by_id(self, id: UUID) -> Optional[Subscription]:
        document = await self._collection.find_one({"_id": id})
        if document: return convert_subscription_dict_to_entity(document)
