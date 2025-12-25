from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.tokens.token import TokenGroup
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import BadRequestException
from app.application.services.jwt_manager import JWTManager
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId


@dataclass(frozen=True)
class RefreshTokenCommand(BaseCommand):
    refresh_token: str | None


@dataclass(frozen=True)
class RefreshTokenCommandHandler(BaseCommandHandler[RefreshTokenCommand, TokenGroup]):
    jwt_manager: JWTManager
    user_repository: BaseUserRepository

    async def handle(self, command: RefreshTokenCommand) -> TokenGroup:

        if command.refresh_token is None:
            raise BadRequestException()

        refresh_token = await self.jwt_manager.validate_token(command.refresh_token)
        user = await self.user_repository.get_by_id(UserId(UUID(refresh_token.sub)))
        if user is None:
            raise

        user_jwt_data = UserJWTData.create_from_user(user)

        return self.jwt_manager.create_token_pair(security_user=user_jwt_data)