from dataclasses import dataclass

from domain.entities.user import User
from infra.repositories.base import BaseMongoDBRepository
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.mongo.convertors import convert_user_document_to_entity, convert_user_entity_to_document


@dataclass
class MongoUserRepository(BaseUserRepository, BaseMongoDBRepository):
    async def create(self, user: User) -> None:
        data = convert_user_entity_to_document(user)
        await self._collection.insert_one(document=data)

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        data = await self._collection.find_one(filter={'tg_id': tg_id})
        if data: return convert_user_document_to_entity(data)