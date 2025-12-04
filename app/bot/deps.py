from typing import Annotated
from aiogram.types import Message, CallbackQuery
from dishka.integrations.aiogram import FromDishka, inject

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.users.get_by_tg_id import GetUserByTgIdQuery
from app.infrastructure.mediator.base import BaseMediator



class UserJWTDataGetter:
    @inject
    async def __call__(
        self,
        mediator: FromDishka[BaseMediator],
        message: Message | CallbackQuery,
    ) -> UserJWTData:
        if message.from_user is None:
            raise

        user_jwt_data: UserJWTData
        user_jwt_data = await mediator.handle_query(
            GetUserByTgIdQuery(telegram_id=message.from_user.id)
        )
        return user_jwt_data

