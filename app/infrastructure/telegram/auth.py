from dataclasses import dataclass
import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qsl

from app.application.dtos.users.web_app import WebAppInitData
from app.application.exception import UnauthorizedException
from app.application.services.telegram import TelegramWebAppAuth


@dataclass
class ITelegramWebAppAuth(TelegramWebAppAuth):
    bot_token: str

    def safe_parse_webapp_init_data(self, init_data: str) -> WebAppInitData:
        if self.check_webapp_signature(init_data):
            return self.    parse_webapp_init_data(init_data)
        raise UnauthorizedException()


    def check_webapp_signature(self, init_data: str) -> bool:

        try:
            parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
        except ValueError:
            return False

        if "hash" not in parsed_data:
            return False

        hash_ = parsed_data.pop("hash")
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(key=b"WebAppData", msg=self.bot_token.encode(), digestmod=hashlib.sha256)
        calculated_hash = hmac.new(
            key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return calculated_hash == hash_

    def parse_webapp_init_data(
        self,
        init_data: str,
        ) -> WebAppInitData:

        result = {}
        for key, value in parse_qsl(init_data):
            if (value.startswith("[") and value.endswith("]")) or (
                value.startswith("{") and value.endswith("}")
            ):
                value = json.loads(value)
            result[key] = value
        return WebAppInitData(**result)
