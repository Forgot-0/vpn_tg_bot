from typing import Any

from domain.entities.order import Order, PaymentStatus
from domain.values.users import UserId
from infrastructure.db.convertors.subscription import (
    convert_subscription_document_to_entity,
    convert_subscription_entity_to_document
)

def convert_order_entity_to_document(order: Order) -> dict[str, Any]:
    return {
        "_id": order.id,
        "subscription": convert_subscription_entity_to_document(order.subscription),
        "user_id": order.user_id.value,
        "total_price": order.total_price,
        "status": order.status.value,
        "payment_id": order.payment_id,
        "payment_date": order.payment_date,
        "created_at": order.created_at,
        "discount": None
    }

def convert_order_document_to_entity(data: dict[str, Any]) -> Order:
    return Order(
        id=data["_id"],
        subscription=convert_subscription_document_to_entity(data["subscription"]),
        user_id=UserId(data["user_id"]),
        total_price=data["total_price"],
        status=PaymentStatus(data["status"]),
        payment_id=data["payment_id"],
        payment_date=data["payment_date"],
        created_at=data["created_at"],
        discount=data["discount"],
    )