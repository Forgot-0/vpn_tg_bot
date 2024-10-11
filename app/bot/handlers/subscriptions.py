from aiogram import F, Router
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from punq import Container

from application.commands.subscriptions.create import CreateSubscriptionCommand
from application.commands.subscriptions.paid import PaidSubscriptionCommand
from application.mediator.mediator import Mediator
from bot.keyboards.tarif import TarifsTextButtons, keyboard_tarifs
from settings.config import Config


router = Router()


@router.message(F.text == 'Купить')
async def buy_sub(message: Message):
    text = """
    Выберите тариф
    """
    await message.answer(
        text=text,
        reply_markup=keyboard_tarifs()
    )


@router.message(F.text == TarifsTextButtons.ONE_MONTH)
async def buy_one_month(message: Message, mediator: Mediator, container: Container):
    text = ""
    subscription, *_ = await mediator.handle_command(
        CreateSubscriptionCommand(
            tg_id=message.from_user.id,
            product=1
        )
    )

    config: Config = container.resolve(Config)
    PRICE = LabeledPrice(label='test', amount=1000)
    await message.answer_invoice(
        title='Test',
        description='Test',
        provider_token=config.bot.provider_token,
        currency='rub',
        is_flexible=False,
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )

@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query_hadnelr(pre_checkout_query: PreCheckoutQuery): 
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def got_payment(message: Message, mediator: Mediator):
    await mediator.handle_command(
        PaidSubscriptionCommand(tg_id=message.from_user.id)
        )
    await message.answer("good")