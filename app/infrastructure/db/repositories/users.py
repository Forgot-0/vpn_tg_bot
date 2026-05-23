from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.users import UserRepository
from app.infrastructure.db.mappers.users import UserMapper
from app.infrastructure.db.models.users import UserModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLAlchemyUserRepository(
    SQLAlchemyRepository[UserModel],
    UserRepository,
):
    model_class = UserModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(UserModel).where(
            UserModel.id == user_id
        )
        user = (await self._session.execute(query)).scalar()
        return UserMapper.to_domain(user) if user else None

    async def add(self, user: User) -> None:
        self._session.add(UserMapper.to_model(user))

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(
            func.lower(UserModel.email) == email.lower()
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.telegram_id == telegram_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def get_by_referral_code(self, referral_code: str) -> User | None:
        stmt = select(UserModel).where(UserModel.referral_code == referral_code)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def list_referrals(self, referrer_id: UUID) -> list[User]:
        stmt = select(UserModel).where(UserModel.referred_by == referrer_id)
        result = await self._session.execute(stmt)
        return [UserMapper.to_domain(m) for m in result.scalars().all()]
