from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.subscriptions import ProductType


@dataclass
class Product(AggregateRoot):
    id: UUID
    code: str
    name: str
    product_type: ProductType
    description: str = ""
    is_active: bool = True
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.code:
            raise ValueError("Product code cannot be empty")
        if not self.name:
            raise ValueError("Product name cannot be empty")

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
