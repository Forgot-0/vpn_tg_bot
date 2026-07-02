from typing import Any

from sqlalchemy import ColumnElement
from sqlalchemy.orm import InstrumentedAttribute, joinedload, lazyload, selectinload, subqueryload

from app.domain.filters.base import BaseFilter
from app.domain.filters.condition import FilterCondition, FilterOperator
from app.domain.filters.exceptions import AttributeNotExistError
from app.domain.filters.loading_strategy import LoadingConfig, LoadingStrategyType, RelationshipLoading
from app.domain.filters.sort import SortField


operators_map = {
    FilterOperator.EQ: lambda a, v: a == v,
    FilterOperator.NE: lambda a, v: a != v,
    FilterOperator.GT: lambda a, v: a > v,
    FilterOperator.GTE: lambda a, v: a >= v,
    FilterOperator.LT: lambda a, v: a < v,
    FilterOperator.LTE: lambda a, v: a <= v,
    FilterOperator.IN: lambda a, v: a.in_(v),
    FilterOperator.NOT_IN: lambda a, v: ~a.in_(v),
    FilterOperator.CONTAINS: lambda a, v: a.ilike(f"%{v}%"),
    FilterOperator.ALL: lambda a, v: a.contains(v),
    FilterOperator.ANY: lambda a, v: a.overlap(v),
    FilterOperator.STARTS_WITH: lambda a, v: a.ilike(f"{v}%"),
    FilterOperator.ENDS_WITH: lambda a, v: a.ilike(f"%{v}"),
    FilterOperator.IS_NULL: lambda a, v: a.is_(None),
    FilterOperator.IS_NOT_NULL: lambda a, v: a.is_not(None),
    FilterOperator.IS_NULL_FROM: lambda a, v: ~a.any(),
    FilterOperator.IS_NOT_NULL_FROM: lambda a, v: a.any(),
}

strategy_map = {
    LoadingStrategyType.LAZY: lambda attr: lazyload(attr),
    LoadingStrategyType.JOINED: lambda attr: joinedload(attr),
    LoadingStrategyType.SELECTIN: lambda attr: selectinload(attr),
    LoadingStrategyType.SUBQUERY: lambda attr: subqueryload(attr),
    LoadingStrategyType.IMMEDIATE: lambda attr: selectinload(attr),
}


class SQLAlchemyFilterConverter:

    @staticmethod
    def get_model_attribute(model: type, field_path: str) -> InstrumentedAttribute:

        parts = field_path.split(".")
        attr = getattr(model, parts[0])

        for part in parts[1:]:
            related_model = attr.property.mapper.class_
            attr = getattr(related_model, part)
        return attr

    @staticmethod
    def condition_to_sqlalchemy(
        model: type,
        condition: FilterCondition
    ) -> ColumnElement[bool]:
        try:
            attr = SQLAlchemyFilterConverter.get_model_attribute(model, condition.field)
        except AttributeError as err:
            raise AttributeNotExistError(field=condition.field) from err

        return operators_map[condition.operator](attr, condition.value)

    @staticmethod
    def filter_to_sqlalchemy_conditions(
        model: type,
        filters: BaseFilter
    ) -> list[ColumnElement[bool]]:
        if not filters.has_conditions():
            return []
        return [
            SQLAlchemyFilterConverter.condition_to_sqlalchemy(model, cond)
            for cond in filters.conditions
        ]

    @staticmethod
    def get_sort_attributes(
        model: type,
        sort_fields: tuple[SortField, ...]
    ) -> list[Any]:
        sort_clauses = []

        for sort_field in sort_fields:
            try:
                attr = SQLAlchemyFilterConverter.get_model_attribute(model, sort_field.field)
                sort_clause = attr.desc() if sort_field.is_descending else attr.asc()
                sort_clauses.append(sort_clause)
            except AttributeError:
                continue

        return sort_clauses

    @staticmethod
    def apply_loading_strategy(
        model: type,
        loading: RelationshipLoading
    ) -> Any:

        try:
            relationship_attr = getattr(model, loading.relationship_name)
        except AttributeError as err:
            raise AttributeNotExistError(field=loading.relationship_name) from err

        loader = strategy_map[loading.strategy](relationship_attr)

        if loading.nested and loading.has_nested:
            related_model = relationship_attr.property.mapper.class_

            for nested in loading.nested:
                nested_loader = SQLAlchemyFilterConverter.apply_loading_strategy(
                    related_model,
                    nested
                )
                loader = loader.options(nested_loader)

        return loader

    @staticmethod
    def build_loading_options(
        model: type,
        loading_config: LoadingConfig
    ) -> list[Any]:

        options = []

        for relationship_loading in loading_config.relationships:
            try:
                loader = SQLAlchemyFilterConverter.apply_loading_strategy(
                    model,
                    relationship_loading
                )
                options.append(loader)
            except ValueError:
                continue

        return options
