from aiogram.types import Update
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import Request, Response
from fastapi.routing import APIRouter

from bot.main import dp, bot
from configs.app import app_settings

router = APIRouter(tags=['webhook'], route_class=DishkaRoute)


@router.post(app_settings.TELEGRAM_WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    secret = (request.headers.get("x-telegram-bot-api-secret-token"))
    if secret != app_settings.WEBHOOK_SECRET or secret is None:
        raise
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_webhook_update(update=update, bot=bot, dishka_container=request.app.state.dishka_container)
    return Response()