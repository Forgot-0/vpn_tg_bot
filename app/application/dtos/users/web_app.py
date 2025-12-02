from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class WebAppChat(BaseModel):
    """
    This object represents a chat.

    Source: https://core.telegram.org/bots/webapps#webappchat
    """

    id: int
    type: str
    title: str
    username: Optional[str] = None
    photo_url: Optional[str] = None



class WebAppUser(BaseModel):
    """
    This object contains the data of the Web App user.

    Source: https://core.telegram.org/bots/webapps#webappuser
    """

    id: int
    is_bot: Optional[bool] = None
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None


class WebAppInitData(BaseModel):
    """
    This object contains data that is transferred to the Web App when it is opened.
    It is empty if the Web App was launched from a keyboard button.

    Source: https://core.telegram.org/bots/webapps#webappinitdata
    """
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)

    query_id: Optional[str] = None
    user: Optional[WebAppUser] = None
    receiver: Optional[WebAppUser] = None

    chat: Optional[WebAppChat] = None

    chat_type: Optional[str] = None
    chat_instance: Optional[str] = None
    start_param: Optional[str] = None
    can_send_after: Optional[int] = None
    auth_date: datetime
    hash: str
