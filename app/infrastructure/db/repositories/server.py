from uuid import UUID

from app.domain.entities.server import Server
from app.domain.filters.server import ServerFilter
from app.domain.repositories.base import PageResult
from app.domain.repositories.servers import BaseServerRepository
from app.domain.values.servers import ProtocolType
from app.infrastructure.db.convertors.filter_converter import MongoFilterConverter
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

    async def update(self, server: Server) -> None:
        doc = convert_server_entity_to_document(server)
        await self._collection.replace_one({"_id": server.id},replacement=doc)

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

    async def get_all_protocols(self) -> list[str]:
        pipeline = [
            {"$project": {"protocol_entries": {"$objectToArray": "$protocol_configs"}}},
            {"$unwind": "$protocol_entries"},
            {"$group": {"_id": None, "protocols": {"$addToSet": "$protocol_entries.k"}}},
            {"$project": {"_id": 0, "protocols": 1}}
        ]
        result = await self._collection.aggregate(pipeline).to_list(length=1)
        return result[0]["protocols"] if result else []

    async def delete_by_id(self, server_id: UUID) -> None:
        await self._collection.delete_one(
            {"_id": server_id}
        )

    async def find_by_filter(self, filters: ServerFilter) -> PageResult[Server]:
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

        servers = tuple(convert_server_document_to_entity(doc) for doc in documents)

        return PageResult(
            items=servers,
            total=total,
            page=filters.pagination.page,
            page_size=filters.pagination.page_size
        )

    async def count_by_filter(self, filters: ServerFilter) -> int:
        query = MongoFilterConverter.filter_to_mongo_query(filters)
        return await self._collection.count_documents(query)