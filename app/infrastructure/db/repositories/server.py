from uuid import UUID

from app.domain.entities.server import Server
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.servers import ProtocolType
from app.infrastructure.db.convertors.server import (
    convert_server_document_to_entity,
    convert_server_entity_to_document
)
from app.infrastructure.db.repositories.base import BaseMongoDBRepository


class ServerRepository(BaseMongoDBRepository, BaseServerRepository):
    async def get_by_max_free(self, type_protocols: list[ProtocolType]) -> Server | None:
        doc = await self._collection.aggregate([
                {
                    "$match": {
                        "$and": [
                            { f'protocol_configs.{protocols.value}': { "$exists": True } } 
                            for protocols in type_protocols
                        ]
                    },
                },
                {"$sort": {"free": 1}},
                { "$limit": 1 }
            ]).to_list(length=1)
        return convert_server_document_to_entity(doc[0]) if doc else None

    async def create(self, server: Server) -> None:
        doc = convert_server_entity_to_document(server)
        await self._collection.insert_one(doc)

    async def update_decrement_free(self, server_id: UUID, decr: int = -1) -> None:
        await self._collection.update_one(
            {"_id": server_id},
            {"$inc": {"free": decr*-1}}
        )

    async def get_all(self) -> list[Server]:
        docs = await self._collection.find().to_list(length=None)
        return [convert_server_document_to_entity(d) for d in docs]

    async def get_by_id(self, server_id: UUID) -> Server | None:
        doc = await self._collection.find_one({"_id": server_id})
        return convert_server_document_to_entity(doc) if doc else None

    async def set_free(self, server_id: UUID, new_free: int) -> None:
        await self._collection.update_one(
            {"_id": server_id},
            {"$set": {"free": new_free}}
        )