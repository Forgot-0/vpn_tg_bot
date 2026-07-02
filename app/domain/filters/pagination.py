from dataclasses import dataclass

from app.domain.filters.exceptions import PaginationParamsError



@dataclass(frozen=True)
class Pagination:
    page: int
    page_size: int

    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    def __post_init__(self) -> None:
        if self.page < 1:
            raise PaginationParamsError(field="page", limit=1)
        if self.page_size < 1:
            raise PaginationParamsError(field="page_size", limit=1)
        if self.page_size > self.MAX_PAGE_SIZE:
            raise PaginationParamsError(field="page_size", limit=self.MAX_PAGE_SIZE)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

    @classmethod
    def default(cls) -> "Pagination":
        return cls(page=cls.DEFAULT_PAGE, page_size=cls.DEFAULT_PAGE_SIZE)

