from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    page: int
    page_size: int

    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    def __post_init__(self):
        if self.page < 1:
            raise
        if self.page_size < 1:
            raise
        if self.page_size > self.MAX_PAGE_SIZE:
            raise

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

    @classmethod
    def default(cls) -> "Pagination":
        return cls(page=cls.DEFAULT_PAGE, page_size=cls.DEFAULT_PAGE_SIZE)

