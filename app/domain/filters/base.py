from abc import ABC
from dataclasses import dataclass, field
from typing import Any

from app.domain.filters.condition import FilterCondition
from app.domain.filters.operators import FilterOperator
from app.domain.filters.pagination import Pagination
from app.domain.filters.sort import SortDirection, SortField


@dataclass
class BaseFilter(ABC):
    _conditions: list[FilterCondition] = field(default_factory=list, init=False)
    _sort_fields: list[SortField] = field(default_factory=list, init=False)
    _pagination: Pagination = field(default_factory=Pagination.default, init=False)

    @property
    def conditions(self) -> tuple[FilterCondition, ...]:
        return tuple(self._conditions)

    @property
    def sort_fields(self) -> tuple[SortField, ...]:
        return tuple(self._sort_fields)

    @property
    def pagination(self) -> Pagination:
        return self._pagination

    def add_condition(
        self,
        field: str,
        operator: FilterOperator,
        value: Any
    ) -> "BaseFilter":
        if value is not None:
            condition = FilterCondition(field=field, operator=operator, value=value)
            self._conditions.append(condition)
        return self

    def set_pagination(self, pagination: Pagination) -> "BaseFilter":
        self._pagination = pagination
        return self

    def add_sort(self, field: str, direction: SortDirection = SortDirection.ASC) -> "BaseFilter":
        sort_field = SortField(field=field, direction=direction)
        self._sort_fields.append(sort_field)
        return self

    def has_conditions(self) -> bool:
        return len(self._conditions) > 0

    def has_sorting(self) -> bool:
        return len(self._sort_fields) > 0

