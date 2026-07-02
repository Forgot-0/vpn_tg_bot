from dataclasses import dataclass
from typing import  Generic, ParamSpec, TypeVar



T = TypeVar("T")
P = ParamSpec("P")


@dataclass(frozen=True)
class PageResult(Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def next_page(self) -> int | None:
        return self.page + 1 if self.has_next else None

    @property
    def previous_page(self) -> int | None:
        return self.page - 1 if self.has_previous else None
