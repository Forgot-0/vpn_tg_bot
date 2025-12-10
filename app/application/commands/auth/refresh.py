from dataclasses import dataclass

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.tokens.token import TokenGroup
from app.application.dtos.users.jwt import UserJWTData
from app.application.services.jwt_manager import JWTManager


@dataclass(frozen=True)
class RefreshTokenCommand(BaseCommand):
    refresh_token: str | None
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class RefreshTokenCommandHandler(BaseCommandHandler[RefreshTokenCommand, TokenGroup]):
    jwt_manager: JWTManager

    async def handle(self, command: RefreshTokenCommand) -> TokenGroup:
        from app.application.exception import BadRequestException

        if command.refresh_token is None:
            raise BadRequestException()

        return await self.jwt_manager.refresh_tokens(
            refresh_token=command.refresh_token,
            security_user=command.user_jwt_data
        )