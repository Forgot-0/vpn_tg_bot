from domain.entities.subscription import Subscription
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.values.subscriptions import SubscriptionId
from infrastructure.db.convertors.subscription import (
    convert_subscription_document_to_entity,
    convert_subscription_entity_to_document
)
from infrastructure.db.repositories.base import BaseMongoDBRepository


class SubscriptionRepository(BaseMongoDBRepository, BaseSubscriptionRepository):
    async def create(self, subscription: Subscription) -> None:
        doc = convert_subscription_entity_to_document(subscription)
        await self._collection.insert_one(doc)

    async def deactivate(self, id: SubscriptionId) -> None:
        await self._collection.update_one(
            {"_id": id.value},
            {"$set": {"active": False}}
        )

    async def activate(self, id: SubscriptionId) -> None:
        await self._collection.update_one(
            {"_id": id.value},
            {"$set": {"active": True}}
        )

    async def get(self) -> list[Subscription]:
        docs = await self._collection.find().to_list(length=None)
        return [convert_subscription_document_to_entity(d) for d in docs]

    async def get_by_id(self, id: SubscriptionId) -> Subscription | None:
        doc = await self._collection.find_one({"_id": id.value})
        return convert_subscription_document_to_entity(doc) if doc else None