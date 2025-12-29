from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.filters.base import BaseFilter
from app.domain.filters.operators import FilterOperator


@dataclass
class PaymentFilter(BaseFilter):
    user_id: UUID | None = None
    subscription_id: UUID | None = None
    status: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    payment_date_after: datetime | None = None
    payment_date_before: datetime | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    has_payment_id: bool | None = None

    def __post_init__(self):
        self._build_conditions()

    def _build_conditions(self) -> None:
        self.add_condition("user_id", FilterOperator.EQ, self.user_id)
        self.add_condition("subscription.id", FilterOperator.EQ, self.subscription_id)
        self.add_condition("status", FilterOperator.EQ, self.status)

        if self.min_price is not None:
            self.add_condition("total_price", FilterOperator.GTE, self.min_price)

        if self.max_price is not None:
            self.add_condition("total_price", FilterOperator.LTE, self.max_price)

        if self.payment_date_after:
            self.add_condition("payment_date", FilterOperator.GTE, self.payment_date_after)

        if self.payment_date_before:
            self.add_condition("payment_date", FilterOperator.LTE, self.payment_date_before)

        if self.created_after:
            self.add_condition("created_at", FilterOperator.GTE, self.created_after)

        if self.created_before:
            self.add_condition("created_at", FilterOperator.LTE, self.created_before)

        if self.has_payment_id is not None:
            operator = FilterOperator.NE if self.has_payment_id else FilterOperator.EQ
            self.add_condition("payment_id", operator, None)

