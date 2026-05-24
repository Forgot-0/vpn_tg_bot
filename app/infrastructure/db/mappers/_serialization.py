from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import TypeVar

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


def dump_optional_str_set(values: frozenset[str] | set[str]) -> list[str]:
    return sorted(values)
