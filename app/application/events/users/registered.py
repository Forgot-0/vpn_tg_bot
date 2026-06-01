from dataclasses import dataclass

from app.application.events.base import BaseEventHandler
from app.application.interfaces.mail import BaseMailService
from app.application.interfaces.token_repository import TokenRepository
from app.domain.events.users import UserCreatedEvent
from app.domain.repositories.users import UserRepository


@dataclass(frozen=True)
class RegisteredEventHandler(BaseEventHandler[UserCreatedEvent, None]):
    user_repository: UserRepository
    mail_service: BaseMailService
    token_repository: TokenRepository

    async def handle(self, event: UserCreatedEvent) -> None:
        ...
