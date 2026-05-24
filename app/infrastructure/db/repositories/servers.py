from typing import FrozenSet
from uuid import UUID

from sqlalchemy import delete, select

from app.domain.entities.server import VPNServer
from app.domain.repositories.servers import VPNServerRepository
from app.domain.values.servers import ProtocolCode
from app.domain.values.subscriptions import PlanFeature
from app.infrastructure.db.mappers.servers import VPNServerMapper
from app.infrastructure.db.models.servers import VPNServerModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLAlchemyVPNServerRepository(
    SQLAlchemyRepository,
    VPNServerRepository,
):
    async def get_by_id(self, server_id: UUID) -> VPNServer | None:
        query = select(VPNServerModel).where(
            VPNServerModel.id == server_id
        )
        server = (await self.session.execute(query)).scalar()
        return VPNServerMapper.to_domain(server) if server else None

    async def add(self, entity: VPNServer) -> None:
        self.session.add(VPNServerMapper.to_model(entity))

    async def update(self, server_entity: VPNServer) -> None:
        query = select(VPNServerModel).where(
            VPNServerModel.id == server_entity.id
        )
        server = (await self.session.execute(query)).scalar()
        if server is None:
            raise ValueError(f"VPNServer {server_entity.id} not found")

        VPNServerMapper.update_model(server, server_entity)

    async def delete(self, server_id: str) -> None:
        await self.session.execute(
            delete(VPNServerModel).where(VPNServerModel.id == server_id)
        )

    async def list_active(self) -> list[VPNServer]:
        stmt = select(VPNServerModel).where(VPNServerModel.is_active.is_(True))
        result = await self.session.execute(stmt)
        return [VPNServerMapper.to_domain(m) for m in result.scalars().all()]

    async def list_by_region(self, region_code: str) -> list[VPNServer]:
        stmt = select(VPNServerModel).where(
            VPNServerModel.region_code == region_code,
            VPNServerModel.is_active.is_(True),
        )
        result = await self.session.execute(stmt)
        return [VPNServerMapper.to_domain(m) for m in result.scalars().all()]

    async def find_supporting(
        self, protocols: FrozenSet[ProtocolCode], features: FrozenSet[PlanFeature]
    ) -> list[VPNServer]:
        protocol_values = [p.value for p in protocols]
        features_values = [f.code.value for f in features]
        stmt = select(VPNServerModel).where(
            VPNServerModel.is_active.is_(True),
            VPNServerModel.supported_protocols.contains(protocol_values),
            VPNServerModel.supported_features.contains(features_values)
        )
        result = await self.session.execute(stmt)
        return [VPNServerMapper.to_domain(m) for m in result.scalars().all()]
