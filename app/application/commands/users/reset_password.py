from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.interfaces.token_repository import TokenRepository
from app.application.interfaces.password import PasswordService
from app.domain.repositories.users import UserRepository
from app.domain.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class ResetPasswordCommand(BaseCommand):
    token: str
    new_password: str
    new_password_repeat: str


@dataclass(frozen=True)
class ResetPasswordCommandHandler(BaseCommandHandler[ResetPasswordCommand, None]):
    token_repository: TokenRepository
    user_repository: UserRepository
    password_service: PasswordService
    uow: UnitOfWork

    async def handle(self, command: ResetPasswordCommand) -> None:
        if command.new_password != command.new_password_repeat:
            raise

        user_id = await self.token_repository.is_valid_token(command.token)
        if user_id is None:
            raise

        user = await self.user_repository.get_by_id(UUID(user_id))
        if user is None:
            raise

        user.password_hash = self.password_service.hash_password(command.new_password)
        await self.user_repository.update(user)
        await self.uow.commit()
        await self.token_repository.invalidate_token(command.token)
