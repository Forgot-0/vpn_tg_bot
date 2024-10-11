from dataclasses import dataclass
from uuid import UUID


@dataclass
class PaginationInfra:
    limit: int = 10
    offset: int = 0
