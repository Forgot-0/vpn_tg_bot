from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.enums import ChatMemberStatus

from configs.app import settings


class CheckSubsChannelMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        # if event.message is None:
        #     return await handler(event, data)

        # chat_member = await data['bot'].get_chat_member(
        #     settings.CHAT_TELEGRAM, user_id=event.message.from_user.id
        #     )

        # if chat_member.status in [
        #     ChatMemberStatus.KICKED,
        #     ChatMemberStatus.LEFT
        # ]: 
        #     await event.message.answer()
        #     return 

        return await handler(event, data)