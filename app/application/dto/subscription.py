from dataclasses import dataclass
from typing import Any
from uuid import UUID

from application.dto.base import BaseDTO
from application.dto.discount import DiscountDTO
from domain.entities.subscription import Subscription


@dataclass
class SubscriptionDTO(BaseDTO):
    id: UUID
    name: str
    description: str
    price: float
    discount: DiscountDTO | None
    price_with_discount: float | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'SubscriptionDTO':
        return SubscriptionDTO(
            id=data['_id'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            discount_id=data['discount_id'],
            price_with_discount=data['price_with_discount'],
        )

    @classmethod
    def from_entity(cls, subscription: Subscription) -> 'SubscriptionDTO':
        return SubscriptionDTO(
            id=subscription.id,
            name=subscription.name,
            description=subscription.description,
            price=subscription.price,
            discount=DiscountDTO.from_entity(subscription.discount) if subscription.discount else None,
            price_with_discount=subscription.price_with_discount
        )