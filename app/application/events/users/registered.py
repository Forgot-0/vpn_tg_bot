from dataclasses import dataclass
from datetime import timedelta
import random

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
        if not event.email:
            return

        code = f"{random.randint(0, 999999):06d}"
        expiration = timedelta(minutes=60)

        await self.token_repository.add_token(code, str(event.user_id), expiration)

        await self.mail_service.send_verification_code(event.email, code, valid_minutes=60)
