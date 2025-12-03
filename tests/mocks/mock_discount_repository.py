from typing import List, Optional
from uuid import UUID
from app.domain.entities.discount import Discount
from app.domain.repositories.discounts import BaseDiscountRepository

class MockDiscountRepository(BaseDiscountRepository):
    def __init__(self):
        self._data: dict[UUID, Discount] = {}

    async def create(self, discount: Discount) -> None:
        self._data[discount.id] = discount

    async def get_by_id(self, id: UUID) -> Optional[Discount]:
        return self._data.get(id)

    async def get(self) -> List[Discount]:
        return list(self._data.values())