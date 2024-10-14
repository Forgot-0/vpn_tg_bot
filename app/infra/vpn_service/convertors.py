from json import dumps
from typing import Any
from domain.events.subscriptions.paid import PaidSubscriptionEvent


def convert_from_event_to_creat_client(event: PaidSubscriptionEvent) -> dict[str, Any]:
    json={
        'id': 1,
        'settings': dumps({
            "clients": [
                {
                    "id": str(event.subscription_id),
                    "flow": "xtls-rprx-vision",
                    "email": str(event.end_time.timestamp()//1),
                    "expiryTime": int(event.end_time.timestamp())*1000,
                    "limitIp": 2,
                    "enable": True,
                }
            ]
        })
    }
    return json