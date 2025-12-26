from dataclasses import dataclass

from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.servers import BaseServerRepository


@dataclass(frozen=True)
class GetListProtocolsQuery(BaseQuery):
    ...


@dataclass(frozen=True)
class GetListProtocolsQueryHandler(BaseQueryHandler[GetListProtocolsQuery, list[str]]):
    servert_repository: BaseServerRepository

    async def handle(self, query: GetListProtocolsQuery) -> list[str]:
        protocols = await self.servert_repository.get_all_protocols()
        return protocols
