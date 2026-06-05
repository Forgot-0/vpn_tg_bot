from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.server import PanelConnection
from app.domain.repositories.panel_connections import PanelConnectionRepository
from app.infrastructure.db.mappers.panel_connections import PanelConnectionMapper
from app.infrastructure.db.models.server_topology import PanelConnectionModel
from app.infrastructure.db.models.servers import VPNServerModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyPanelConnectionRepository(SQLAlchemyRepository, PanelConnectionRepository):

    async def get_by_id(self, connection_id: UUID) -> PanelConnection | None:
        model = await self.session.get(PanelConnectionModel, connection_id)
        return PanelConnectionMapper.to_entity(model) if model else None

    async def get_by_server(self, server_id: UUID) -> PanelConnection | None:
        stmt = (
            select(PanelConnectionModel)
            .join(
                VPNServerModel,
                VPNServerModel.panel_connection_id == PanelConnectionModel.id,
            )
            .where(VPNServerModel.id == server_id)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PanelConnectionMapper.to_entity(model) if model else None

    async def list_active(self) -> list[PanelConnection]:
        stmt = select(PanelConnectionModel).where(
            PanelConnectionModel.is_active.is_(True)
        )
        result = await self.session.execute(stmt)
        return [
            PanelConnectionMapper.to_entity(m) for m in result.scalars().all()
        ]

    async def add(self, connection: PanelConnection) -> None:
        self.session.add(PanelConnectionMapper.to_model(connection))

    async def update(self, connection: PanelConnection) -> None:
        model = await self.session.get(PanelConnectionModel, connection.id)
        if model is None:
            raise
        PanelConnectionMapper.update_model(model, connection)

    async def delete(self, connection_id: UUID) -> None:
        model = await self.session.get(PanelConnectionModel, connection_id)
        if model is not None:
            await self.session.delete(model)
