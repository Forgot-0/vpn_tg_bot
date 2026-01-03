
from dataclasses import dataclass
import logging
from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.tokens.token import TokenGroup
from app.application.dtos.users.jwt import UserJWTData
from app.application.services.jwt_manager import JWTManager
from app.application.services.telegram import safe_parse_webapp_init_data
from app.domain.entities.user import User
from app.domain.repositories.users import BaseUserRepository
from app.application.exception import BadRequestException


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class LoginTelegramUserCommand(BaseCommand):
    init_data: str


@dataclass(frozen=True)
class LoginTelegramUserCommandHandler(BaseCommandHandler[LoginTelegramUserCommand, TokenGroup]):
    user_repository: BaseUserRepository
    jwt_manager: JWTManager

    async def handle(self, command: LoginTelegramUserCommand) -> TokenGroup:
        user_data = safe_parse_webapp_init_data(command.init_data)
        if user_data.user is None:
            raise BadRequestException()

        user = await self.user_repository.get_by_telegram_id(telegram_id=user_data.user.id)
        if user is None:
            user = User.create(
                telegram_id=user_data.user.id,
                is_premium=user_data.user.is_premium,
                username=user_data.user.username,
                fullname=f"{user_data.user.first_name}-{user_data.user.last_name}"
            )

        logger.info(
            "Logining by telegram", extra={"user_id": user.id, "telegram_id": user.telegram_id}
        )

        return self.jwt_manager.create_token_pair(UserJWTData.create_from_user(user))
