from bot.messages.base import BaseMessageBuilder
from bot.messages.menu import get_menu_keyboards





class StartMessageBuilder(BaseMessageBuilder):
    _text = (
        "👋 Привет! Я бот для продажи впн \n"
        "Используй меню:"
    )
    _reply_markup = get_menu_keyboards()