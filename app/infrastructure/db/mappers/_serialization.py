from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import TypeVar, cast

from app.domain.values.money import Money

E = TypeVar("E", bound=StrEnum)


def dump_enum_set(values: frozenset[StrEnum] | set[StrEnum]) -> list[str]:
    return sorted(item.value for item in values)


def load_enum_set(raw: list[str] | None, enum_cls: type[E]) -> frozenset[E]:
    if not raw:
        return frozenset()
    return frozenset(enum_cls(value) for value in raw)


def dump_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value)


def load_decimal(value: str | int | float | None) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))


def dump_money(value: Money | None) -> dict[str, str] | None:
    if value is None:
        return None
    return {"amount": str(value.amount), "currency": value.currency}


def load_money(raw: dict[str, str] | None) -> Money | None:
    if raw is None:
        return None
    return Money(amount=Decimal(str(raw["amount"])), currency=raw["currency"])


def dump_money_list(values: set[Money] | list[Money] | None) -> list[dict[str, str]]:
    if not values:
        return []

    return [cast(dict[str, str], dump_money(item)) for item in sorted(values, key=lambda item: (item.currency, item.amount))]


def load_money_set(raw: list[dict[str, str]] | None) -> set[Money]:
    if not raw:
        return set()
    return {cast(Money, load_money(item)) for item in raw if item is not None}


def dump_optional_str_set(values: frozenset[str] | set[str]) -> list[str]:
    return sorted(values)
