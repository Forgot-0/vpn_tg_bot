from app.domain.entities.server import Server
from app.domain.entities.subscription import Subscription
from app.domain.filters.subscription import SubscriptionFilter
from app.domain.repositories.base import PageResult
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId
from app.infrastructure.db.convertors.filter_converter import MongoFilterConverter
from app.infrastructure.db.convertors.subscription import (
    convert_subscription_document_to_entity,
    convert_subscription_entity_to_document
)
from app.infrastructure.db.repositories.base import BaseMongoDBRepository


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

    async def get_by_user(self, user_id: UserId) -> list[Subscription]:
        docs = await self._collection.find(
            {"user_id": user_id.value}
        ).to_list(length=None)
        return [convert_subscription_document_to_entity(d) for d in docs]

    async def update(self, subscription: Subscription) -> None:
        doc = convert_subscription_entity_to_document(subscription)
        await self._collection.replace_one({"_id": subscription.id.value}, doc, upsert=True)

    async def find_by_filter(self, filters: SubscriptionFilter) -> PageResult[Subscription]:
        query = MongoFilterConverter.filter_to_mongo_query(filters)

        sort = (
            MongoFilterConverter.sort_to_mongo(filters.sort_fields)
        )

        total = await self._collection.count_documents(query)

        cursor = self._collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        cursor = cursor.skip(filters.pagination.offset)
        cursor = cursor.limit(filters.pagination.limit)

        documents = await cursor.to_list(length=filters.pagination.limit)

        servers = tuple(convert_subscription_document_to_entity(doc) for doc in documents)

        return PageResult(
            items=servers,
            total=total,
            page=filters.pagination.page,
            page_size=filters.pagination.page_size
        )

    async def count_by_filter(self, filters: SubscriptionFilter) -> int:
        query = MongoFilterConverter.filter_to_mongo_query(filters)
        return await self._collection.count_documents(query)