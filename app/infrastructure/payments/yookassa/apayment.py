from dataclasses import dataclass
from ipaddress import ip_address, ip_network
import logging
from typing import Any
from uuid import UUID

from httpx import AsyncClient
import orjson


from app.configs.app import app_settings
from app.domain.entities.payment import Payment
from app.application.services.payment import BasePaymentService, PaymentAnswer
from app.application.exception import BadRequestException, ForbiddenException


logger = logging.getLogger(__name__)

@dataclass
class YooKassaPaymentService(BasePaymentService):
    _client: AsyncClient
    API_BASE: str = "https://api.yookassa.ru"

    NETWORKS: list[str] = [
        "77.75.153.0/25",
        "77.75.156.11",
        "77.75.156.35",
        "77.75.154.128/25",
        "185.71.76.0/27",
        "185.71.77.0/27",
        "2a02:5180:0:1509::/64",
        "2a02:5180:0:2655::/64",
        "2a02:5180:0:1533::/64",
        "2a02:5180:0:2669::/64",
    ]

    def __init__(self, shop_id: str, api_key: str) -> None:
        self._client = AsyncClient(
            base_url=self.API_BASE, auth=(shop_id, api_key)
        )


    async def create(self, order: Payment) -> PaymentAnswer:
        headers = {
            'Idempotence-Key': str(order.id),
        }

        data = {
            'amount': {
                'value': order.total_price,
                'currency': 'RUB',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': f'https://t.me/{app_settings.BOT_USERNAME}'
            },
            'capture': True,
            "customization": {
                "payment_methods": ['bank_card', 'sbp']
            },
            'metadata': {
                'order_id': str(order.id)
            },
            "description": f"Подписка vpn за {order.total_price}"

        }

        response = await self._client.post("v3/payments", json=data, headers=headers)
        response.raise_for_status()
        data = orjson.loads(response.content)
        return PaymentAnswer(url=data['confirmation']['confirmation_url'], payment_id=data['id'])

    async def check(self, payment_id: UUID) -> dict[str, str]:
        response = await self._client.get(f"v3/payments/{payment_id}")
        response.raise_for_status()
        data = orjson.loads(response.content)

        return data['metadata']

    def _is_ip_in_network(self, ip: str, network: str) -> bool:
        try:
            return ip_address(ip) in ip_network(network, strict=False)
        except Exception as exception:
            logger.error(f"Failed to check IP '{ip}' in network '{network}': {exception}")
            return False

    def _is_ip_trusted(self, ip: str) -> bool:
        return any(self._is_ip_in_network(ip, net) for net in self.NETWORKS)


    async def handle_webhook(self, playload: dict[str, Any], headers: dict[str, Any]) -> UUID:
        data = playload.get("object")
        if data is None:
            raise

        payment_id = data.get("id")
        if payment_id is None:
            raise

        ip = (
            headers.get("CF-Connecting-IP")
            or headers.get("X-Real-IP")
            or headers.get("X-Forwarded-For")
        )

        if ip is None:
            raise BadRequestException()

        if self._is_ip_trusted(ip) is False:
            raise ForbiddenException()

        return UUID(payment_id)
