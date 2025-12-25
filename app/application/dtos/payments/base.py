from dataclasses import dataclass, field
from typing import Literal

from app.application.dtos.base import FilterParam, ListParams, SortParam


@dataclass
class PaymentSortParam(SortParam):
    field: Literal["id", "created_at", "payment_date", "total_price"]


@dataclass
class PaymentFilterParam(FilterParam):
    field: Literal["id", "user_id", "total_price", "payment_id"]


@dataclass
class PaymentListParams(ListParams):
    sort: list[PaymentSortParam] | None = field(default=None)
    filters: list[PaymentFilterParam] | None = field(default=None)


