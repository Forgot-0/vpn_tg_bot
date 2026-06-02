from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import BusinessRuleViolationError
from app.domain.values.money import Money
from app.domain.values.subscriptions import OfferStatus


@dataclass
class Offer(AggregateRoot):
    id: UUID
    plan_id: UUID
    price_id: UUID
    title: str
    subtitle: str = ""
    marketing_labels: tuple[str, ...] = ()
    terms: str = ""
    status: OfferStatus = OfferStatus.DRAFT
    discount_percent: Decimal | None = None
    trial_days: int | None = None
    sort_order: int = 0
    active_from: date | None = None
    active_to: date | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.title:
            raise ValueError("Offer title cannot be empty")
        if self.discount_percent is not None and not Decimal("0") <= self.discount_percent <= Decimal("100"):
            raise ValueError("Offer discount_percent must be between 0 and 100")
        if self.trial_days is not None and self.trial_days < 0:
            raise ValueError("Offer trial_days cannot be negative")

    def activate(self) -> None:
        self.status = OfferStatus.ACTIVE

    def archive(self) -> None:
        self.status = OfferStatus.ARCHIVED

    def ensure_available(self, today: date) -> None:
        if self.status != OfferStatus.ACTIVE:
            raise BusinessRuleViolationError(reason="Offer is not active")
        if self.active_from is not None and today < self.active_from:
            raise BusinessRuleViolationError(reason="Offer is not active yet")
        if self.active_to is not None and today > self.active_to:
            raise BusinessRuleViolationError(reason="Offer is expired")

    def apply_discount(self, money: Money) -> Money:
        if self.discount_percent is None:
            return money
        multiplier = (Decimal("100") - self.discount_percent) / Decimal("100")
        return Money((money.amount * multiplier).quantize(Decimal("0.01")), money.currency)
