
from typing import Any

from domain.entities.subscription import ProductType, Subscription


def convert_subscription_dict_to_entity(document: dict[str, Any]) -> Subscription:
    return Subscription(
        id=document['_id'],
        tg_id=document['tg_id'],
        server_id=document['server_id'],
        product=ProductType(document['product']),
        amount=document['amount'],
        end_time=document['end_time'],
        created_at=document['created_at'],
        is_pay=document['is_pay'],
        vpn_url=document['vpn_url'],
        payment_id=document['payment_id']
    )

def convert_subscription_entity_to_dict(subscription: Subscription) -> dict[str, Any]:
    return {
        '_id': subscription.id,
        'tg_id': subscription.tg_id,
        'server_id': subscription.server_id,
        'product': subscription.product.value,
        'amount': subscription.amount,
        'end_time': subscription.end_time,
        'created_at': subscription.created_at,
        'is_pay': subscription.is_pay,
        'vpn_url': subscription.vpn_url,
        'payment_id': subscription.payment_id
    }