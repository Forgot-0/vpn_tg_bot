
from json import dumps
from typing import Any
from uuid import UUID
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.vpn_service.schema import Settings


def convert_from_event_to_creat_client(event: PaidSubscriptionEvent, user_id: UUID) -> dict[str, Any]:
    json={
        'id': 1,
        'settings': dumps({
            "clients": [
                {
                    "id": str(user_id),
                    "flow": "xtls-rprx-vision",
                    "email": str(event.tg_id),
                    "expiryTime": int(event.end_time.timestamp())*1000,
                    "limitIp": 1,
                    "enable": True,
                }
            ]
        })
    }
    return json