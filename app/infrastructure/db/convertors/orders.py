from typing import Any
from domain.entities.order import Order
from infrastructure.db.convertors.discounts import (
    convert_discount_dict_to_entity,
    convert_discount_entity_to_dict
)
from infrastructure.db.convertors.subscriptions import (
    convert_subscription_dict_to_entity,
    convert_subscription_entity_to_dict
)


def convert_order_entity_to_dict(order: Order) -> dict:
    return {
        '_id': order.id,
        'subscription': convert_subscription_entity_to_dict(order.subscription),
        'user_id': order.user_id,
        'total_price': order.total_price,
        'payment_date': order.payment_date,
        'payment_id': order.payment_id,
        'created_at': order.created_at,
        'discount': convert_discount_entity_to_dict(order.discount) if order.discount else None
    }


def convert_order_dict_to_entity(document: dict[str, Any]) -> Order:
    return Order(
        id=document['_id'],
        subscription=convert_subscription_dict_to_entity(document['subscription']),
        user_id=document['user_id'],
        total_price=document['total_price'],
        payment_date=document['payment_date'],
        payment_id=document['payment_id'],
        created_at=document['created_at'],
        discount=convert_discount_dict_to_entity(document['discount']) if document.get('discount') else None
    )

