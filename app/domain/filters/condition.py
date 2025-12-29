from dataclasses import dataclass
from typing import Any

from app.domain.filters.operators import FilterOperator


@dataclass(frozen=True)
class FilterCondition:
    field: str
    operator: FilterOperator
    value: Any

    def __post_init__(self):
        if not self.field:
            raise 

        if self.value is None:
            raise 

