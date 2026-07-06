from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.server import VPNServer
from app.domain.repositories.filter import PageResult
from app.domain.repositories.servers import ServerFilter, ServerRepository
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.infrastructure.db.mappers.server import ServerMapper
from app.infrastructure.db.models.server import VPNServerModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLServerRepository(SQLAlchemyRepository, ServerRepository):
    async def get_by_id(self, server_id: UUID) -> VPNServer | None:
        result = await self.session.execute(select(VPNServerModel).where(VPNServerModel.id == server_id))
        server_model = result.scalar()
        return ServerMapper.from_server_model_to_domain(server_model) if server_model is not None else None

    async def list_active(self) -> list[VPNServer]:
        result = await self.session.execute(select(VPNServerModel).where(VPNServerModel.is_active.is_(True)))
        return [ServerMapper.from_server_model_to_domain(model) for model in result.scalars()]

    async def list_filtered(self, *, filter: ServerFilter) -> PageResult[VPNServer]:
        query = select(VPNServerModel)

        if filter.name:
            query = query.where(VPNServerModel.name.ilike(f"%{filter.name}%"))

        if filter.panel_type is not None:
            query = query.where(VPNServerModel.panel_type == filter.panel_type.value)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.execute(count_query)).scalar_one()

        paged_query = query.limit(filter.pagination.limit).offset(filter.pagination.offset)
        result = await self.session.execute(paged_query)

        return PageResult(
            items=[ServerMapper.from_server_model_to_domain(model) for model in result.scalars()],
            total=total,
            page=filter.pagination.page,
            page_size=filter.pagination.page_size,
        )

    async def list_capable(
        self,
        *,
        protocols: frozenset[ProtocolCode],
        features: frozenset[FeatureCode],
    ) -> list[VPNServer]:
        query = select(VPNServerModel)

        if protocols:
            query = query.where(VPNServerModel.support_protocols.contains([protocol.value for protocol in protocols]))

        if features:
            query = query.where(VPNServerModel.support_features.contains([feature.value for feature in features]))

        result = await self.session.execute(query)
        return [ServerMapper.from_server_model_to_domain(model) for model in result.scalars()]

    async def add(self, server: VPNServer) -> None:
        self.session.add(ServerMapper.from_server_domain_to_model(server))

    async def update(self, server: VPNServer) -> None:
        await self.session.merge(ServerMapper.from_server_domain_to_model(server))

    async def delete(self, server_id: UUID) -> None:
        await self.session.execute(delete(VPNServerModel).where(VPNServerModel.id == server_id))
