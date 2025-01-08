from typing import Any

from domain.entities.discount import Discount, DiscountUser


def convert_discount_entity_to_dict(discount: Discount) -> dict[str, Any]:
    return {
        '_id': discount.id,
        'name': discount.name,
        'description': discount.description,
        'percent': discount.percent,
        'conditions': discount.conditions,
        'uses': discount.uses,
        'is_active': discount.is_active
    }


def convert_discount_dict_to_entity(data: dict[str, Any]) -> Discount:
    return Discount(
        id=data['_id'],
        name=data['name'],
        description=data['description'],
        percent=data['percent'],
        conditions=data['conditions'],
        uses=data['uses'],
        is_active=data['is_active']
    )

def convert_discount_user_dict_to_entity(data: dict[str, Any]) -> DiscountUser:
    return DiscountUser(
        discount_id=data['discount_id'],
        user_id=data['user_id'],
        count=data['count']
    )

def convert_discount_user_entity_to_dict(discount_user: DiscountUser) -> dict[str, Any]:
    return {
        'discount_id': discount_user.discount_id,
        'user_id': discount_user.user_id,
        'count': discount_user.count
    }