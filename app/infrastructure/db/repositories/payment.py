from datetime import datetime
from uuid import UUID
from app.domain.entities.payment import Payment, PaymentStatus
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.services.utils import now_utc
from app.infrastructure.db.convertors.payment import (
    convert_order_document_to_entity, convert_order_entity_to_document
)
from app.infrastructure.db.repositories.base import BaseMongoDBRepository


class PaymentRepository(BaseMongoDBRepository, BasePaymentRepository):
    async def create(self, payment: Payment) -> None:
        doc = convert_order_entity_to_document(payment)
        await self._collection.insert_one(doc)

    async def pay(self, id: UUID) -> None:
        await self._collection.update_one(
            {"_id": id},
            {"$set": {"status": PaymentStatus.succese.value, "payment_date": now_utc()}}
        )

    async def get_by_id(self, id: UUID) -> Payment | None:
        doc = await self._collection.find_one({"_id": id})
        return convert_order_document_to_entity(doc) if doc else None

    async def get_by_user_id(self, user_id: int) -> list[Payment]:
        cursor = self._collection.find({"user_id": user_id})
        docs = await cursor.to_list(length=None)
        return [convert_order_document_to_entity(d) for d in docs]

    async def update(self, payment: Payment) -> None:
        doc = convert_order_entity_to_document(payment)
        await self._collection.replace_one({"_id": payment.id}, doc)
    
    async def get_by_payment_id(self, payment_id: UUID) -> Payment | None:
        document = await self._collection.find_one({"payment_id": payment_id})
        return convert_order_document_to_entity(document) if document else None
