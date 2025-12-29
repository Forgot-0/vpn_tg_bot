from app.domain.entities.user import User
from app.domain.filters.user import UserFilter
from app.domain.repositories.base import PageResult
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId
from app.infrastructure.db.convertors.filter_converter import MongoFilterConverter
from app.infrastructure.db.convertors.users import convert_user_document_to_entity, convert_user_entity_to_document
from app.infrastructure.db.repositories.base import BaseMongoDBRepository


class UserRepository(BaseMongoDBRepository, BaseUserRepository):
    async def create(self, user: User) -> None:
        doc = convert_user_entity_to_document(user)
        await self._collection.insert_one(doc)

    async def get_by_id(self, id: UserId) -> User | None:
        doc = await self._collection.find_one({"_id": id.value})
        return convert_user_document_to_entity(doc) if doc else None

    async def update(self, user: User) -> None:
        doc = convert_user_entity_to_document(user)
        await self._collection.replace_one({"_id": user.id.value}, doc)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        doc = await self._collection.find_one({"telegram_id": telegram_id})
        return convert_user_document_to_entity(doc) if doc else None

    async def find_by_filter(self, filters: UserFilter) -> PageResult[User]:
        query = MongoFilterConverter.filter_to_mongo_query(filters)

        sort = (
            MongoFilterConverter.sort_to_mongo(filters.sort_fields)
            if filters.has_sorting()
            else [("created_at", -1)]
        )

        total = await self._collection.count_documents(query)

        cursor = self._collection.find(query)
        cursor = cursor.sort(sort)
        cursor = cursor.skip(filters.pagination.offset)
        cursor = cursor.limit(filters.pagination.limit)

        documents = await cursor.to_list(length=filters.pagination.limit)
        
        users = tuple(convert_user_document_to_entity(doc) for doc in documents)

        return PageResult(
            items=users,
            total=total,
            page=filters.pagination.page,
            page_size=filters.pagination.page_size
        )

    async def count_by_filter(self, filters: UserFilter) -> int:
        query = MongoFilterConverter.filter_to_mongo_query(filters)
        return await self._collection.count_documents(query)