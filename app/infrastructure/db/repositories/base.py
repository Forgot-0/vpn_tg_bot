from abc import ABC
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient

from app.application.dtos.base import ListParams, SortOrder



@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def build_query(self, params: ListParams):
        query = {}

        if params.filters:
            for filter_param in params.filters:
                field = filter_param.field
                value = filter_param.value

                if isinstance(value, list):
                    query[field] = {"$in": value}
                else:
                    query[field] = value

        sort = []
        if params.sort:
            for sort_param in params.sort:
                order = 1 if sort_param.order == SortOrder.ASC else -1
                sort.append((sort_param.field, order))

        if not sort:
            sort = [("_id", 1)]

        return query, sort

    async def get_paginated_items(self, params: ListParams):
        query, sort = await self.build_query(params)

        skip = (params.page - 1) * params.page_size
        limit = params.page_size

        cursor = self._collection.find(query).sort(sort).skip(skip).limit(limit)
        items = await cursor.to_list(length=params.page_size)

        total = await self._collection.count_documents(query)

        pagination = {
            "total": total,
            "page": params.page,
            "page_size": params.page_size
        }

        return {"items": items, "pagination": pagination}