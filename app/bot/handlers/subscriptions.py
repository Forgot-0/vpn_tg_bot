from aiogram import F, Router
from aiogram.types import Message, PreCheckoutQuery
from punq import Container

from application.commands.subscriptions.create import CreateSubscriptionCommand
from application.commands.subscriptions.paid import PaidSubscriptionCommand
from application.mediator.mediator import Mediator
from application.queries.subscriptions.get_active_subs import GetAllActiveSubsQuery
from bot.keyboards.tarif import TarifsTextButtons, keyboard_tarifs
from bot.texts.subscriptions import SubscriptionText
from bot.utils import send_invoice
from domain.entities.subscription import ProductType, Subscription


router = Router()


@router.message(F.text =='Купить')
async def buy_sub(message: Message):
    await message.answer(
        text=SubscriptionText.BUY,
        reply_markup=keyboard_tarifs()
    )


@router.message(F.text.in_([tarif.value for tarif in TarifsTextButtons]))
async def buy_one_month(message: Message, mediator: Mediator, container: Container):
    subscription, *_ = await mediator.handle_command(
        CreateSubscriptionCommand(
            tg_id=message.from_user.id,
            product=getattr(ProductType, str(TarifsTextButtons(message.text).name))
        )
    )
    await send_invoice(container=container, message=message, subscription=subscription)


@router.message(F.text=="/get_active_vpn_url")
async def get_active_vpn_url(message: Message, mediator: Mediator):
    vpn_urls: list[Subscription] = await mediator.handle_query(GetAllActiveSubsQuery(tg_id=message.from_user.id))
    if not vpn_urls: 
        await message.answer(text=SubscriptionText.NOT_ACTIVE_SUB) 
        return
    
    for vpn in vpn_urls:
        await message.answer(text=SubscriptionText.get_vpn_url_text(vpn=vpn), parse_mode='MarkdownV2')


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query_hadnelr(pre_checkout_query: PreCheckoutQuery): 
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def got_payment(message: Message, mediator: Mediator):
    await mediator.handle_command(
        PaidSubscriptionCommand(
            tg_id=message.from_user.id, 
            payment_id=message.successful_payment.provider_payment_charge_id
            )
        )