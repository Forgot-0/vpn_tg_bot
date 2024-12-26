from aiogram import F, Router
from aiogram.types import Message

from bot.messages.menu import MenuTextButtons
from bot.messages.referral import ReferralMessage


router = Router()


@router.message(F.text==MenuTextButtons.REF)
async def referral_message(message: Message):
    data = ReferralMessage().build(user_id=message.from_user.id)
    await message.answer(**data)


