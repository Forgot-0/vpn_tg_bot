from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.server import VPNServer
from app.domain.repositories.servers import VPNServerRepository
from app.infrastructure.db.mappers.servers import VPNServerMapper
from app.infrastructure.db.models.servers import VPNServerModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLAlchemyVPNServerRepository(SQLAlchemyRepository, VPNServerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, server_id: UUID) -> VPNServer | None:
        model = await self.session.get(VPNServerModel, server_id)
        return VPNServerMapper.to_entity(model) if model else None

    async def add(self, server: VPNServer) -> None:
        self.session.add(VPNServerMapper.to_model(server))

    async def update(self, server: VPNServer) -> None:
        model = await self.session.get(VPNServerModel, server.id)
        if model is None:
            raise LookupError(f"VPNServer {server.id} not found")
        VPNServerMapper.update_model(model, server)

    async def delete(self, server_id: UUID) -> None:
        await self.session.execute(delete(VPNServerModel).where(VPNServerModel.id == server_id))

    async def list_active(self) -> list[VPNServer]:
        stmt = select(VPNServerModel).where(VPNServerModel.is_active.is_(True))
        result = await self.session.execute(stmt)
        return [VPNServerMapper.to_entity(model) for model in result.scalars().all()]

    async def list_by_region(self, region_code: str) -> list[VPNServer]:
        stmt = select(VPNServerModel).where(VPNServerModel.region_code == region_code)
        result = await self.session.execute(stmt)
        return [VPNServerMapper.to_entity(model) for model in result.scalars().all()]
