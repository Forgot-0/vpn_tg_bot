from dataclasses import dataclass
from datetime import datetime

from app.domain.filters.base import BaseFilter
from app.domain.filters.operators import FilterOperator


@dataclass
class UserFilter(BaseFilter):
    telegram_id: int | None = None
    role: str | None = None
    is_premium: bool | None = None
    username: str | None = None
    fullname: str | None = None
    phone: str | None = None
    referred_by_id: str | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    has_subscriptions: bool | None = None
    min_referrals_count: int | None = None

    def __post_init__(self):
        self._build_conditions()

    def _build_conditions(self) -> None:
        self.add_condition("telegram_id", FilterOperator.EQ, self.telegram_id)
        self.add_condition("role", FilterOperator.EQ, self.role)
        self.add_condition("is_premium", FilterOperator.EQ, self.is_premium)
        self.add_condition("referred_by", FilterOperator.EQ, self.referred_by_id)

        if self.username:
            self.add_condition("username", FilterOperator.CONTAINS, self.username)

        if self.fullname:
            self.add_condition("fullname", FilterOperator.CONTAINS, self.fullname)

        if self.phone:
            self.add_condition("phone", FilterOperator.CONTAINS, self.phone)

        if self.created_after:
            self.add_condition("created_at", FilterOperator.GTE, self.created_after)

        if self.created_before:
            self.add_condition("created_at", FilterOperator.LTE, self.created_before)

        if self.min_referrals_count is not None:
            self.add_condition("referrals_count", FilterOperator.GTE, self.min_referrals_count)

        if self.has_subscriptions is not None:
            operator = FilterOperator.NE if self.has_subscriptions else FilterOperator.EQ
            self.add_condition("subscriptions", operator, [])
