from datetime import timedelta
from uuid import UUID
from domain.entities.subscription import Subscription


def convert_subscription_entity_to_dict(subscription: Subscription) -> dict:
    return {
        "_id": subscription.id,
        "name": subscription.name,
        "description": subscription.description,
        "limit_ip": subscription.limit_ip,
        "limit_trafic": subscription.limit_trafic,
        "duration": subscription.duration.total_seconds(),
        "price": subscription.price,
        "is_active": subscription.is_active,
    }

def convert_subscription_dict_to_entity(data: dict) -> Subscription:
    return Subscription(
        id=data["_id"],
        name=data["name"],
        description=data['description'],
        limit_ip=data["limit_ip"],
        limit_trafic=data["limit_trafic"],
        duration=timedelta(seconds=data["duration"]),
        price=data["price"],
        is_active=data["is_active"],
    )
