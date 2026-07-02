from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from app.domain.filters.condition import FilterCondition, FilterOperator
from app.domain.filters.loading_strategy import LoadingConfig, LoadingStrategyType, RelationshipLoading
from app.domain.filters.pagination import Pagination
from app.domain.filters.sort import SortDirection, SortField



@dataclass
class BaseFilter(ABC):
    _conditions: list[FilterCondition] = field(default_factory=list, init=False)
    _sort_fields: list[SortField] = field(default_factory=list, init=False)
    _pagination: Pagination = field(default_factory=Pagination.default, init=False)
    _relation: dict[str, RelationshipLoading] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.build_conditions()

    @abstractmethod
    def build_conditions(self) -> None:
        ...

    @property
    def conditions(self) -> tuple[FilterCondition, ...]:
        return tuple(self._conditions)

    @property
    def sort_fields(self) -> tuple[SortField, ...]:
        return tuple(self._sort_fields)

    @property
    def pagination(self) -> Pagination:
        return self._pagination

    @property
    def loading_config(self) -> LoadingConfig:
        cfg = LoadingConfig(tuple(self._relation.values()))
        return cfg

    def add_condition(
        self,
        field: str,
        operator: FilterOperator,
        value: Any
    ) -> "BaseFilter":
        if operator in (
            FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL,
            FilterOperator.IS_NULL_FROM, FilterOperator.IS_NOT_NULL_FROM
        ):
            condition = FilterCondition(field=field, operator=operator, value=None)
            self._conditions.append(condition)
        elif value is not None:
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

    def add_relation(
        self,
        name: str,
        strategy: LoadingStrategyType=LoadingStrategyType.SELECTIN,
        *nesteds: str
    ) -> None:

        self._relation[name] = (
            RelationshipLoading(
                relationship_name=name,
                strategy=strategy,
                nested=tuple(RelationshipLoading(rel, strategy=strategy) for rel in nesteds)
                if nesteds else None
            )
        )

    def has_conditions(self) -> bool:
        return len(self._conditions) > 0

    def has_sorting(self) -> bool:
        return len(self._sort_fields) > 0

