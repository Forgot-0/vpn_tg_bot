from typing import Any
from uuid import UUID
from domain.entities.subscription import Subscription
from domain.values.servers import ProtocolType, Region
from domain.values.subscriptions import SubscriptionId


def convert_subscription_entity_to_document(subscription: Subscription) -> dict[str, Any]:
    return {
            "_id": subscription.id.value,
            "duration": subscription.duration,
            "start_date": subscription.start_date,
            "device_count": subscription.device_count,
            "server_id": str(subscription.server_id),
            "region": {
                "flag": subscription.region.flag,
                "name": subscription.region.name,
                "code": subscription.region.code
            },
            "protocol_types": [pt.value for pt in subscription.protocol_types],
            "active": subscription.is_active(),
        }

def convert_subscription_document_to_entity(data: dict[str, Any]) -> Subscription:
    return Subscription(
            id=SubscriptionId(data["_id"]),
            duration=data["duration"],
            start_date=data["start_date"],
            device_count=data["device_count"],
            server_id=UUID(data["server_id"]),
            region=Region(**data["region"]),
            protocol_types=[ProtocolType(pt) for pt in data["protocol_types"]]
        )
