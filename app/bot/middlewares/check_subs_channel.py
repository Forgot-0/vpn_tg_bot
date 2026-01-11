from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Update


class CheckSubsChannelMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:

        return await handler(event, data)