from dataclasses import dataclass
from datetime import datetime
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
        data = await self._collection.find_one({'_id': id, 'is_pay': False})
        if data: return convert_subscription_dict_to_entity(data)

    async def get_by_tg_id(self, tg_id: int) -> Subscription | None:
        data = await self._collection.find_one({'tg_id': tg_id, 'is_pay': False})
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

    async def set_payment_id(self, id: UUID, payment_id: str) -> str:
        await self._collection.update_one(
            filter={
                '_id': id
            },
            update={
                "$set": {'payment_id': payment_id}
            }
        )

    async def delete_not_paid_sub(self, tg_id: int) -> None:
        await self._collection.delete_many(
            filter={
                'tg_id': tg_id,
                'is_pay': False
            }
        )

    async def get_active_subscription(self, tg_id: int) -> list[Subscription] | None:
        documents = await self._collection.find(
            {   
                'tg_id': tg_id,
                'is_pay': True,
                'end_time': {'$gt': datetime.now()}
            }
        ).to_list(length=None)

        if documents: return [convert_subscription_dict_to_entity(document) for document in documents]

    async def set_vpn_url(self, subs_id: UUID, vpn_url: str) -> None:
        await self._collection.update_one(
            filter={
                '_id': subs_id
            },
            update={
                '$set': {'vpn_url': vpn_url}
            }
        )