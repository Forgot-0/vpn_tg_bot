from aiogram.types import LabeledPrice, Message
from punq import Container

from domain.entities.subscription import Subscription
from settings.config import Config


async def send_invoice(container: Container, message: Message, subscription: Subscription):
    config: Config = container.resolve(Config)
    PRICE = LabeledPrice(label='test', amount=subscription.amount*100)
    await message.answer_invoice(
        title=f'Подписка на {message.text.replace('На', '', 1)}',
        description='Покупка ссылки на vpn vless',
        provider_token=config.bot.provider_token,
        currency='rub',
        is_flexible=False,
        prices=[PRICE],
        payload='some-invoice-payload-for-our-internal-use'
    )
