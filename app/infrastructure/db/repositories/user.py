from uuid import UUID

from sqlalchemy import select

from app.domain.entities.user import User
from app.domain.repositories.users import UserRepository
from app.infrastructure.db.mappers.users import UserMapper
from app.infrastructure.db.models.user import UserModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLUserRepository(SQLAlchemyRepository, UserRepository):
    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id==user_id)
        )
        return UserMapper.from_user_model_to_domain(result.scalar())

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email==email)
        )
        return UserMapper.from_user_model_to_domain(result.scalar())

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id==telegram_id)
        )
        return UserMapper.from_user_model_to_domain(result.scalar())

    async def get_by_referral_code(self, code: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.referral_code==code)
        )
        return UserMapper.from_user_model_to_domain(result.scalar())

    async def add(self, user: User) -> None:
        self.session.add(UserMapper.from_user_domain_to_mode(user))

    async def update(self, user: User) -> None:
        ...

    async def list_referrals(self, referrer_id: UUID) -> list[User]:
        results = await self.session.execute(
            select(UserModel).where(UserModel.referred_by==referrer_id)
        )
        return [UserMapper.from_user_model_to_domain(user) for user in results.scalars()]

