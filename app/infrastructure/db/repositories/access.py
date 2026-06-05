from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.access import ProvisionedAccess
from app.domain.repositories.access import ProvisionedAccessRepository
from app.infrastructure.db.mappers.access import ProvisionedAccessMapper
from app.infrastructure.db.models.access import ProvisionedAccessModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyProvisionedAccessRepository(SQLAlchemyRepository, ProvisionedAccessRepository):
    async def get_by_id(self, access_id: UUID) -> ProvisionedAccess | None:
        model = await self.session.get(ProvisionedAccessModel, access_id)
        return ProvisionedAccessMapper.to_entity(model) if model else None

    async def list_by_subscription(self, subscription_id: UUID) -> list[ProvisionedAccess]:
        stmt = select(ProvisionedAccessModel).where(
            ProvisionedAccessModel.subscription_id == subscription_id
        )
        result = await self.session.execute(stmt)
        return [ProvisionedAccessMapper.to_entity(model) for model in result.scalars().all()]

    async def add(self, access: ProvisionedAccess) -> None:
        self.session.add(ProvisionedAccessMapper.to_model(access))

    async def update(self, access: ProvisionedAccess) -> None:
        model = await self.session.get(ProvisionedAccessModel, access.id)
        if model is None:
            raise LookupError(f"ProvisionedAccess {access.id} not found")
        updated = ProvisionedAccessMapper.to_model(access)
        for key, value in updated.__dict__.items():
            if not key.startswith("_"):
                setattr(model, key, value)
