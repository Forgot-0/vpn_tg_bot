from aiogram.types import Update
from fastapi import Request, Response
from fastapi.routing import APIRouter

from bot.main import dp, bot
from configs.app import app_settings

router = APIRouter()


@router.post(app_settings.TELEGRAM_WEBHOOK_PATH)
async def telegram_webhook(requests: Request):
    update = Update.model_validate(await requests.json(), context={"bot": bot})
    await dp.feed_update(update=update, bot=bot)
    return Response()