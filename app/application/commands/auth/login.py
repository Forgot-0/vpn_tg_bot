
from dataclasses import dataclass
from application.commands.base import BaseCommand, BaseCommandHandler
from application.dtos.tokens.token import TokenGroup
from application.dtos.users.jwt import UserJWTData
from application.services.jwt_manager import JWTManager
from application.services.telegram import safe_parse_webapp_init_data
from domain.entities.user import User
from domain.repositories.users import BaseUserRepository



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
            raise

        user = await self.user_repository.get_by_telegram_id(telegram_id=user_data.user.id)
        if user:
            return self.jwt_manager.create_token_pair(UserJWTData.create_from_user(user))

        user = User.create(
            telegram_id=user_data.user.id,
            is_premium=user_data.user.is_premium,
            username=user_data.user.username,
            fullname=f"{user_data.user.first_name}-{user_data.user.last_name}"
        )

        return self.jwt_manager.create_token_pair(UserJWTData.create_from_user(user))