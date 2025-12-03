from pydantic import BaseModel


class LoginTelegram(BaseModel):
    init_data: str