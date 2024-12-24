
from dataclasses import dataclass

from domain.entities.user import User
from domain.repositories.users import BaseUserRepository
from infrastructure.db.convertors.users import convert_user_document_to_entity, convert_user_entity_to_document
from infrastructure.db.repositories.base import BaseMongoDBRepository


@dataclass
class MongoUserRepository(BaseUserRepository, BaseMongoDBRepository):
    async def create(self, user: User) -> None:
        data = convert_user_entity_to_document(user)
        await self._collection.insert_one(document=data)

    async def get_by_id(self, id: int) -> User | None:
        data = await self._collection.find_one(filter={'_id': id})
        if data: return convert_user_document_to_entity(data)

