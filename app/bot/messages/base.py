from typing import Any


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