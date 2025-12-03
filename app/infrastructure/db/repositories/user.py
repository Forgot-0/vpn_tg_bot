from app.application.dtos.base import PaginatedResult, Pagination
from app.application.dtos.users.base import UserListParams
from app.domain.entities.user import User
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId
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

    async def get_list(self, filter_params: UserListParams) -> PaginatedResult[User]:
        documents = await self.get_paginated_items(params=filter_params)
        users = [convert_user_document_to_entity(doc) for doc in documents['items']]
        return PaginatedResult(
            items=users,
            pagination=Pagination(**documents["pagination"])
        )