from typing import Any
from uuid import UUID

from app.domain.filters.base import BaseFilter
from app.domain.filters.condition import FilterCondition
from app.domain.filters.operators import FilterOperator
from app.domain.filters.sort import SortField


class MongoFilterConverter:

    @staticmethod
    def condition_to_mongo(condition: FilterCondition) -> dict[str, Any]:
        operators_map = {
            FilterOperator.EQ: lambda v: v,
            FilterOperator.NE: lambda v: {"$ne": v},
            FilterOperator.GT: lambda v: {"$gt": v},
            FilterOperator.GTE: lambda v: {"$gte": v},
            FilterOperator.LT: lambda v: {"$lt": v},
            FilterOperator.LTE: lambda v: {"$lte": v},
            FilterOperator.IN: lambda v: {"$in": v},
            FilterOperator.NOT_IN: lambda v: {"$nin": v},
            FilterOperator.CONTAINS: lambda v: {"$regex": v, "$options": "i"},
            FilterOperator.STARTS_WITH: lambda v: {"$regex": f"^{v}", "$options": "i"},
            FilterOperator.ENDS_WITH: lambda v: {"$regex": f"{v}$", "$options": "i"},
        }

        mongo_value = operators_map[condition.operator](condition.value)
        return {condition.field: mongo_value}

    @staticmethod
    def filter_to_mongo_query(filters: BaseFilter) -> dict[str, Any]:
        if not filters.has_conditions():
            return {}

        conditions = [
            MongoFilterConverter.condition_to_mongo(cond)
            for cond in filters.conditions
        ]

        if len(conditions) == 1:
            return conditions[0]

        return {"$and": conditions}

    @staticmethod
    def sort_to_mongo(sort_fields: tuple[SortField, ...]) -> list[tuple[str, int]]:
        return [
            (field.field, -1 if field.is_descending else 1)
            for field in sort_fields
        ]
