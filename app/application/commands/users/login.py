from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users import TokenGroup, UserJWTData
from app.application.interfaces.auth import JWTManager
from app.application.interfaces.password import PasswordService
from app.domain.errors import InvalidCredentialsError
from app.domain.repositories.users import UserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginCommand(BaseCommand):
    username: str
    password: str


@dataclass(frozen=True)
class LoginCommandHandler(BaseCommandHandler[LoginCommand, TokenGroup]):
    user_repository: UserRepository
    jwt_manager: JWTManager
    password_service: PasswordService

    async def handle(self, command: LoginCommand) -> TokenGroup:
        user = await self.user_repository.get_by_email(command.username)

        if user is None or (
            user is not None
            and user.password_hash is not None
            and self.password_service.verify_password(command.password, user.password_hash)
        ):
            raise InvalidCredentialsError()

        token_group = self.jwt_manager.create_token_pair(
            UserJWTData.create_from_user(user, device_id=None)
        )

        logger.info("User logged in", extra={"user_id": user.id})
        return token_group
