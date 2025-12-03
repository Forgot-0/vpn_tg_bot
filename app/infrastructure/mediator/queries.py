from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Type

from app.application.queries.base import QR, BaseQuery, BaseQueryHandler



@dataclass
class QueryRegistry:
    quries_map: dict[Type[BaseQuery], Type[BaseQueryHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_query(self, query: Type[BaseQuery], type_handler: Type[BaseQueryHandler]) -> None:
        self.quries_map[query] = type_handler

    def get_handler_types(self, query: BaseQuery) -> Type[BaseQueryHandler]:
        if query.__class__ not in self.quries_map:
            raise 

        return self.quries_map[query.__class__]


@dataclass(eq=False)
class QueryMediator(ABC):
    query_registy: QueryRegistry

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...
