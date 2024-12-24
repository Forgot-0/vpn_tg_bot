from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.user import User
from domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    id: int
    is_premium: bool
    username: str | None
    fullname: str | None
    phone: str | None


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler[CreateUserCommand, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: CreateUserCommand) -> None:
        if await self.user_repository.get_by_id(id=command.id):
            return

        user = User(
            id=command.id,
            is_premium=command.is_premium,
            username=command.username,
            fullname=command.fullname,
            phone=command.phone
        )

        await self.user_repository.create(user=user)
        await self.mediator.publish(user.pull_events())