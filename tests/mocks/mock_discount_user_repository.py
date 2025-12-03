from typing import Optional
from uuid import UUID
from app.domain.entities.discount import DiscountUser
from app.domain.repositories.discounts import BaseDiscountUserRepository
from app.domain.values.users import UserId


class MockDiscountUserRepository(BaseDiscountUserRepository):
    def __init__(self):
        self._data: dict[tuple[UUID, UserId], DiscountUser] = {}

    async def create(self, discount_user: DiscountUser) -> None:
        key = (discount_user.discount_id, discount_user.user_id)
        self._data[key] = discount_user

    async def get_by_discount_user(self, discount_id: UUID, user_id: UserId) -> Optional[DiscountUser]:
        return self._data.get((discount_id, user_id))

    async def incr_count(self, discount_id: UUID, user_id: UserId, incr: int = 1) -> None:
        key = (discount_id, user_id)
        discount_user = self._data.get(key)
        if discount_user:
            if hasattr(discount_user, "count"):
                discount_user.count += incr
            else:
                discount_user.count = incr
            self._data[key] = discount_user