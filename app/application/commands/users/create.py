from dataclasses import dataclass
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.user import User
from domain.repositories.users import BaseUserRepository
from domain.values.users import UserId


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    tg_id: int
    is_premium: bool
    username: str | None
    fullname: str | None
    phone: str | None
    referred_by: UUID | None


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler[CreateUserCommand, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: CreateUserCommand) -> None:

        user = User.create(
            telegram_id=command.tg_id,
            is_premium=command.is_premium,
            username=command.username,
            fullname=command.fullname,
            phone=command.phone,
            referred_by=UserId(command.referred_by) if command.referred_by else None
        )

        await self.user_repository.create(user=user)
        await self.mediator.publish(user.pull_events())