from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.user import User
from domain.repositories.servers import BaseServerRepository
from domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    id: int
    is_premium: bool
    username: str | None
    fullname: str | None
    phone: str | None
    referred_by: int | None


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler[CreateUserCommand, None]):
    user_repository: BaseUserRepository
    server_reposiptry: BaseServerRepository

    async def handle(self, command: CreateUserCommand) -> None:
        if await self.user_repository.get_by_id(id=command.id):
            return

        server = await self.server_reposiptry.get_by_max_free()

        user = User.create(
            id=command.id,
            server_id=server.id,
            is_premium=command.is_premium,
            username=command.username,
            fullname=command.fullname,
            phone=command.phone,
            referred_by=command.referred_by
        )

        await self.user_repository.create(user=user)
        await self.mediator.publish(user.pull_events())