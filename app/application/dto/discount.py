from dataclasses import dataclass
from typing import Any
from uuid import UUID

from application.dto.base import BaseDTO
from domain.entities.discount import Discount


@dataclass
class DiscountDTO(BaseDTO):
    id: UUID
    name: str
    description: str
    percent: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'DiscountDTO':
        return super().from_dict(data)

    @classmethod
    def from_entity(cls, entity: Discount) -> 'DiscountDTO':
        return DiscountDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            percent=entity.percent
        )