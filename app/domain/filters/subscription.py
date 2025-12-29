from dataclasses import dataclass
from datetime import datetime

from app.domain.filters.base import BaseFilter
from app.domain.filters.operators import FilterOperator


@dataclass
class SubscriptionFilter(BaseFilter):
    user_id: str| None = None
    server_id: str| None = None
    region_code: str| None = None
    status: str| None = None
    protocol_types: list[str] | None = None
    min_duration: int| None = None
    max_duration: int| None = None
    start_date_after: datetime | None = None
    start_date_before: datetime | None = None
    min_device_count: int| None = None
    max_device_count: int| None = None

    def __post_init__(self):
        self._build_conditions()

    def _build_conditions(self) -> None:
        self.add_condition("user_id", FilterOperator.EQ, self.user_id)
        self.add_condition("server_id", FilterOperator.EQ, self.server_id)
        self.add_condition("region.code", FilterOperator.EQ, self.region_code)
        self.add_condition("status", FilterOperator.EQ, self.status)

        if self.protocol_types:
            self.add_condition("protocol_types", FilterOperator.IN, self.protocol_types)

        if self.min_duration is not None:
            self.add_condition("duration", FilterOperator.GTE, self.min_duration)

        if self.max_duration is not None:
            self.add_condition("duration", FilterOperator.LTE, self.max_duration)

        if self.min_device_count is not None:
            self.add_condition("device_count", FilterOperator.GTE, self.min_device_count)

        if self.max_device_count is not None:
            self.add_condition("device_count", FilterOperator.LTE, self.max_device_count)

        if self.start_date_after:
            self.add_condition("start_date", FilterOperator.GTE, self.start_date_after)

        if self.start_date_before:
            self.add_condition("start_date", FilterOperator.LTE, self.start_date_before)
