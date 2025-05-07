from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from infrastructure.depends.init import get_mediator, init_container


class MediatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data['mediator'] = get_mediator()
        data['container'] = init_container()

        return await handler(event, data)