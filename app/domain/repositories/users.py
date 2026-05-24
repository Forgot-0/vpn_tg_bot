from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...
 
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...
 
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...
 
    @abstractmethod
    async def get_by_referral_code(self, code: str) -> User | None: ...
 
    @abstractmethod
    async def add(self, user: User) -> None: ...
 
    @abstractmethod
    async def update(self, user: User) -> None: ...
 
    @abstractmethod
    async def list_referrals(self, referrer_id: UUID) -> list[User]: ...
 