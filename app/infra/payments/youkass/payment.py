from dataclasses import dataclass
from uuid import UUID
import aiohttp


from domain.entities.subscription import Subscription
from infra.payments.base import BasePaymentService


@dataclass
class YouKassaPaymentService(BasePaymentService):
    auth_base64: str

    async def create(self, subscription: Subscription) -> tuple[str, str]:
        url = 'https://api.yookassa.ru/v3/payments'

        headers = {
            'Idempotence-Key': str(subscription.id),
            'Authorization': f'Basic {self.auth_base64}'
        }

        payment = {
            'amount': {
                'value': subscription.amount,
                'currency': 'RUB',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://t.me/forgot_vpn_bot'
            },
            'capture': True,
            'metadata': {
                'tg_id': subscription.tg_id,
                'subscription_id': str(subscription.id)

            },
            "description": f"Подписка vpn за {subscription.amount}"

        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payment, headers=headers) as response:
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