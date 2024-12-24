from dataclasses import dataclass
from uuid import UUID
import aiohttp


from domain.entities.order import Order
from infrastructure.payments.base import BasePaymentService


@dataclass
class YooKassaPaymentService(BasePaymentService):
    auth_base64: str

    async def create(self, order: Order) -> tuple[str, str]:
        url = 'https://api.yookassa.ru/v3/payments'

        headers = {
            'Idempotence-Key': str(order.id),
            'Authorization': f'Basic {self.auth_base64}'
        }

        data = {
            'amount': {
                'value': order.total_price,
                'currency': 'RUB',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://t.me/forgot_vpn_bot'
            },
            'capture': True,
            'metadata': {
                'order_id': str(order.id)

            },
            "description": f"Подписка vpn за {order.total_price}"

        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                result = await response.json()
                return result['confirmation']['confirmation_url'], result['id']


    async def check(self, payment_id: UUID) -> dict[str, str]:
        url = f'https://api.yookassa.ru/v3/payments/{payment_id}'

        headers = {
            'Authorization': f'Basic {self.auth_base64}',
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:

                if response.status == 200:
                    payment = await response.json()
                    return payment['metadata']

                else:
                    error_response = await response.json()
                    raise