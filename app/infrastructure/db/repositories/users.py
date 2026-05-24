from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.users import UserRepository
from app.infrastructure.db.mappers.users import UserMapper
from app.infrastructure.db.models.users import UserModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLAlchemyUserRepository(SQLAlchemyRepository, UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        model = await self.session.get(UserModel, user_id)
        return UserMapper.to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def get_by_referral_code(self, code: str) -> User | None:
        stmt = select(UserModel).where(UserModel.referral_code == code)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def add(self, user: User) -> None:
        self.session.add(UserMapper.to_model(user))

    async def update(self, user: User) -> None:
        model = await self.session.get(UserModel, user.id)
        if model is None:
            raise LookupError(f"User {user.id} not found")
        UserMapper.update_model(model, user)

    async def list_referrals(self, referrer_id: UUID) -> list[User]:
        stmt = select(UserModel).where(UserModel.referred_by == referrer_id)
        result = await self.session.execute(stmt)
        return [UserMapper.to_entity(model) for model in result.scalars().all()]
