from dataclasses import dataclass
from uuid import UUID

from domain.entities.subscription import Subscription
from infra.repositories.base import BaseMongoDBRepository
from infra.repositories.subscriptions.base import BaseSubscriptionRepository
from infra.repositories.subscriptions.mongo.convertors import (
    convert_subscription_dict_to_entity, 
    convert_subscription_entity_to_dict
)


@dataclass
class MongoSubscriptionRepository(BaseSubscriptionRepository, BaseMongoDBRepository):

    async def create(self, subscription: Subscription) -> None:
        document = convert_subscription_entity_to_dict(subscription)
        await self._collection.insert_one(document=document)

    async def get_by_id(self, id: UUID) -> Subscription | None:
        data = await self._collection.find_one({'_id': id})
        if data: return convert_subscription_dict_to_entity(data)

    async def get_by_tg_id(self, tg_id: int) -> Subscription | None:
        data = await self._collection.find_one({'tg_id': tg_id})
        if data: return convert_subscription_dict_to_entity(data)

    async def pay(self, id: UUID) -> None:
        await self._collection.update_one(
            filter={
                '_id': id
            },
            update={
                "$set": {'is_pay': True}
            }
        )