from aiogram.types import Message, CallbackQuery

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.users.get_by_tg_id import GetUserByTgIdQuery
from app.infrastructure.mediator.base import BaseMediator
from app.application.exception import BadRequestException





async def user_jwt_getter(
    mediator: BaseMediator,
    message: Message | CallbackQuery,
) -> UserJWTData:
    if message.from_user is None:
        raise BadRequestException()

    user_jwt_data: UserJWTData
    user_jwt_data = await mediator.handle_query(
        GetUserByTgIdQuery(telegram_id=message.from_user.id)
    )
    return user_jwt_data

