from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.event_bus import EventBus
from app.application.interfaces.password import PasswordService
from app.domain.entities.user import User
from app.domain.errors import (
    UserAlreadyExistsError,
    PasswordMismatchError,
)
from app.domain.repositories.uow import UnitOfWork
from app.domain.repositories.users import UserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RegisterUserByEmailCommand(BaseCommand):
    email: str
    password: str
    password_repeat: str
    referral_code: str


@dataclass(frozen=True)
class RegisterUserByEmailCommandHandler(BaseCommandHandler[RegisterUserByEmailCommand, None]):
    user_repository: UserRepository
    password_service: PasswordService
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: RegisterUserByEmailCommand) -> None:
        if command.password != command.password_repeat:
            raise PasswordMismatchError

        email_user = await self.user_repository.get_by_email(command.email)
        if email_user is not None:
            raise UserAlreadyExistsError

        reffered_user_id = None
        if command.referral_code:
            reffered_user = await self.user_repository.get_by_referral_code(command.referral_code)
            if reffered_user is not None:
                reffered_user.increment_referrals()
                reffered_user_id = reffered_user.id
                await self.user_repository.update(reffered_user)

        password_hash = self.password_service.hash_password(command.password)
        user = User.create(
            email=command.email,
            password_hash=password_hash,
            referred_by=reffered_user_id
        )

        await self.user_repository.add(user)
        await self.uow.commit()
        await self.event_bus.publish(user.pull_events())
