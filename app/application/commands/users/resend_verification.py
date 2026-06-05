from dataclasses import dataclass
import secrets
from datetime import timedelta

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.interfaces.mail import BaseMailService
from app.application.interfaces.token_repository import TokenRepository
from app.domain.repositories.users import UserRepository


@dataclass(frozen=True)
class ResendVerificationCommand(BaseCommand):
    email: str


@dataclass(frozen=True)
class ResendVerificationCommandHandler(BaseCommandHandler[ResendVerificationCommand, None]):
    user_repository: UserRepository
    token_repository: TokenRepository
    mail_service: BaseMailService

    async def handle(self, command: ResendVerificationCommand) -> None:
        user = await self.user_repository.get_by_email(command.email)
        if user is None or user.email is None:
            raise

        code = f"{secrets.randbelow(10**6):06d}"
        expiration = timedelta(minutes=60)
        await self.token_repository.add_token(code, str(user.id), expiration)

        await self.mail_service.send_verification_code(user.email, code, valid_minutes=60)
