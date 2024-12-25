from dataclasses import dataclass
from uuid import UUID

from domain.entities.server import Server
from domain.repositories.servers import BaseServerRepository
from infrastructure.db.convertors.servers import convert_server_dict_to_entity, convert_server_entity_to_dict
from infrastructure.db.repositories.base import BaseMongoDBRepository

@dataclass
class MongoServerRepository(BaseServerRepository, BaseMongoDBRepository):

    async def get_by_max_free(self) -> Server | None:
        document = await self._collection.find().sort({'free': 1}).to_list(length=1)
        if document: return convert_server_dict_to_entity(document[0])

    async def create(self, server: Server) -> None:
        document = convert_server_entity_to_dict(server)
        await self._collection.insert_one(document=document)

    async def update_decrement_free(self, server_id: UUID) -> None:
        await self._collection.update_one(
            filter={
                '_id': server_id
            },
            update={
                '$inc': {'free': -1}
            }
        )

    async def get_all(self) -> list[Server]:
        documents = await self._collection.find().to_list(length=None)
        return [convert_server_dict_to_entity(document) for document in documents]

    async def get_by_id(self, server_id: UUID) -> Server | None:
        document = await self._collection.find_one({'_id': server_id})
        if document: return convert_server_dict_to_entity(document)

    async def set_free(self, server_id: UUID, new_free: int) -> None:
        await self._collection.update_one(
            filter={
                '_id': server_id
            },
            update={
                '$set': {'free': new_free}
            }
        )
