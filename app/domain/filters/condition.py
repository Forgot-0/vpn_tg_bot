from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.domain.filters.exceptions import ValueMustNotNoneError



class FilterOperator(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    LIKE = "like"
    ILIKE = "ilike"
    CONTAINS = "contains"
    ALL = "all"
    ANY = "any"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    IS_NULL_FROM = "is_null_from"
    IS_NOT_NULL_FROM = "is_not_null_from"


null_set = {
    FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL,
    FilterOperator.IS_NULL_FROM, FilterOperator.IS_NOT_NULL_FROM
}

@dataclass(frozen=True)
class FilterCondition:
    field: str
    operator: FilterOperator
    value: Any

    def __post_init__(self) -> None:
        if self.value is None and self.operator not in null_set:
            raise ValueMustNotNoneError(field=self.field)
