from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.user import User
from infra.repositories.users.base import BaseUserRepository


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    tg_id: int
    is_premium: bool
    tg_username: str | None = None  


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler[User, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: User) -> None:
        user = User.create(
            tg_id=command.tg_id,
            is_premium=command.is_premium,
            tg_username=command.tg_username
        )

        await self.user_repository.create(user=user)
        await self.mediator.publish(user.pull_events())
