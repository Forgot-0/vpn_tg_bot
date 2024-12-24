from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.order import Order
from domain.repositories.orders import BaseOrderRepository
from infrastructure.db.convertors.orders import convert_order_dict_to_entity, convert_order_entity_to_dict
from infrastructure.db.repositories.base import BaseMongoDBRepository


@dataclass
class MongoOrderRepository(BaseOrderRepository, BaseMongoDBRepository):
    async def create(self, order: Order) -> None:
        document = convert_order_entity_to_dict(order)
        await self._collection.insert_one(document=document)

    async def pay(self, id: UUID) -> None:
        await self._collection.update_one(
            {'_id': id}, 
            {
                "$set":
                    {
                        'payment_date': datetime.now(),
                    }
            }
        )

    async def get_by_id(self, id: UUID) -> Order | None:
        document = await self._collection.find_one(filter={'_id': id})
        if document: return convert_order_dict_to_entity(document)

    async def get_by_user_id(self, user_id: int) -> list[Order]:
        current_date = datetime.now()
        documents = await self._collection.find(
            {
                "user_id": user_id,
                "$expr": {
                    "$gte": [
                        { "$add": ["$payment_date", "$subscription.duration"] },
                        current_date
                    ]
                }
            }
        ).to_list(length=None)
        if documents: return [convert_order_dict_to_entity(document) for document in documents]