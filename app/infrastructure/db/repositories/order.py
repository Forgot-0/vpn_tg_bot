from datetime import datetime
from uuid import UUID
from domain.entities.order import Order, PaymentStatus
from domain.repositories.orders import BaseOrderRepository
from infrastructure.db.convertors.order import (
    convert_order_document_to_entity, convert_order_entity_to_document
)
from infrastructure.db.repositories.base import BaseMongoDBRepository


class OrderRepository(BaseMongoDBRepository, BaseOrderRepository):
    async def create(self, order: Order) -> None:
        doc = convert_order_entity_to_document(order)
        await self._collection.insert_one(doc)

    async def pay(self, id: UUID) -> None:
        await self._collection.update_one(
            {"_id": id},
            {"$set": {"status": PaymentStatus.succese.value, "payment_date": datetime.now()}}
        )

    async def get_by_id(self, id: UUID) -> Order | None:
        doc = await self._collection.find_one({"_id": id})
        return convert_order_document_to_entity(doc) if doc else None

    async def get_by_user_id(self, user_id: int) -> list[Order]:
        cursor = self._collection.find({"user_id": user_id})
        docs = await cursor.to_list(length=None)
        return [convert_order_document_to_entity(d) for d in docs]

    async def update(self, order: Order) -> None:
        doc = convert_order_entity_to_document(order)
        await self._collection.replace_one({"_id": order.id}, doc)