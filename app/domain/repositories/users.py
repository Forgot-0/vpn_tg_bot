from abc import abstractmethod
from uuid import UUID

from app.domain.entities.user import User
from app.domain.repositories.base import Repository
from app.domain.values.users import UserId


class UserRepository(Repository[User, UserId]):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_referral_code(self, referral_code: str) -> User | None: ...

    @abstractmethod
    async def list_referrals(self, referrer_id: UserId) -> list[User]: ...
