from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import InvalidStateTransitionError
from app.domain.values.money import Money
from app.domain.values.subscriptions import OrderStatus


@dataclass(frozen=True)
class OrderLineItem:
    product_id: UUID
    plan_id: UUID | None
    price_id: UUID | None
    offer_id: UUID | None
    title: str
    quantity: int
    unit_price: Money
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise ValueError("Order line item quantity must be >= 1")
        if self.unit_price.amount <= 0:
            raise ValueError("Order line item unit price must be positive")

    @property
    def total(self) -> Money:
        return Money(self.unit_price.amount * Decimal(self.quantity), self.unit_price.currency)


@dataclass
class Order(AggregateRoot):
    id: UUID
    user_id: UUID
    line_items: list[OrderLineItem]
    status: OrderStatus = OrderStatus.DRAFT
    total: Money | None = None
    checkout_session_id: UUID | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.line_items:
            raise ValueError("Order must contain at least one line item")
        currencies = {item.unit_price.currency for item in self.line_items}
        if len(currencies) != 1:
            raise ValueError("Order line items must use a single currency")

    def recalculate_total(self) -> Money:
        currency = self.line_items[0].unit_price.currency
        amount = sum((item.total.amount for item in self.line_items), Decimal("0"))
        self.total = Money(amount, currency)
        return self.total

    def mark_pending_payment(self) -> None:
        self._require_status({OrderStatus.DRAFT}, action="mark pending payment")
        self.recalculate_total()
        self.status = OrderStatus.PENDING_PAYMENT

    def mark_paid(self) -> None:
        self._require_status({OrderStatus.PENDING_PAYMENT}, action="mark paid")
        self.status = OrderStatus.PAID

    def mark_fulfilling(self) -> None:
        self._require_status({OrderStatus.PAID}, action="mark fulfilling")
        self.status = OrderStatus.FULFILLING

    def complete(self) -> None:
        self._require_status({OrderStatus.PAID, OrderStatus.FULFILLING}, action="complete")
        self.status = OrderStatus.COMPLETED

    def cancel(self) -> None:
        if self.status in {OrderStatus.COMPLETED, OrderStatus.REFUNDED}:
            raise InvalidStateTransitionError(reason=f"Cannot cancel order in status {self.status}")
        self.status = OrderStatus.CANCELLED

    def _require_status(self, allowed: set[OrderStatus], *, action: str) -> None:
        if self.status not in allowed:
            raise InvalidStateTransitionError(reason=f"Cannot {action} order in status {self.status}")
