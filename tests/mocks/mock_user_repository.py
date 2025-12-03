from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserId


class MockUserRepository(BaseUserRepository):
    def __init__(self):
        self._data: dict[UserId, User] = {}

    async def create(self, user: User) -> None:
        self._data[user.id] = user

    async def get_by_id(self, id: UserId) -> Optional[User]:
        return self._data.get(id)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        for user in self._data.values():
            if user.telegram_id == telegram_id:
                return user
        return None

    async def update(self, user: User) -> None:
        self._data[user.id] = user