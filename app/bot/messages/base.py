from typing import Any

from aiogram.types import InputMediaPhoto

from app.bot.static.init import photo_manager



class BaseMessageBuilder:
    _text: str = ""
    _reply_markup: Any = None
    _parse_mode: str | None = None

    @property
    def text(self) -> str:
        return self._text

    @property
    def reply_markup(self) -> Any | None:
        return self._reply_markup

    @property
    def parse_mode(self) -> str | None:
        return self._parse_mode 

    def build(self) -> dict[str, Any]:
        content = {"text": self.text}

        if self.reply_markup:
            content["reply_markup"] = self.reply_markup

        if self.parse_mode:
            content["parse_mode"] = self.parse_mode

        return content

class BaseMediaBuilder:
    _photo: str = ""
    _caption: str = ""
    _reply_markup: Any = None

    @property
    def photo(self) -> str:
        return self._photo

    @property
    def reply_markup(self) -> Any | None:
        return self._reply_markup

    @property
    def caption(self) -> str:
        return self._caption

    def build(self) -> dict[str, Any]:
        content = {}

        media = InputMediaPhoto(media=photo_manager.get_image_id(self.photo), caption=self.caption)
        content['media'] = media

        if self.reply_markup:
            content["reply_markup"] = self.reply_markup

        return content
