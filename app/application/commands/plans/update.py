from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users import UserJWTData
from app.domain.errors import PlanNotFoundError
from app.domain.repositories.plans import PlanRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.services.access_control import RoleAccessControl
from app.domain.values.subscriptions import PlanVisibility
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UpdatePlanCommand(BaseCommand):
    user_jwt_data: UserJWTData
    plan_id: UUID

    name: str | None = None
    description: str | None = None
    visibility: PlanVisibility | None = None
    order_index: int | None = None
    is_active: bool | None = None
    is_trial: bool | None = None


@dataclass(frozen=True)
class UpdatePlanCommandHandler(BaseCommandHandler[UpdatePlanCommand, None]):
    plan_repository: PlanRepository
    access_service: RoleAccessControl
    uow: UnitOfWork

    async def handle(self, command: UpdatePlanCommand) -> None:
        if not self.access_service.can_action(command.user_jwt_data.role, UserRole.ADMIN):
            raise 

        plan = await self.plan_repository.get_by_id(command.plan_id)
        if plan is None:
            raise PlanNotFoundError(entity_id=str(command.plan_id))

        if command.name is not None:
            plan.name = command.name

        if command.description is not None:
            plan.description = command.description

        if command.visibility is not None:
            plan.visibility = command.visibility

        if command.order_index is not None:
            plan.order_index = command.order_index

        if command.is_active is not None:
            plan.is_active = command.is_active

        if command.is_trial is not None:
            plan.is_trial = command.is_trial

        await self.plan_repository.update(plan)
        await self.uow.commit()

        logger.info(
            "Updated plan",
            extra={
                "updated_by": str(command.user_jwt_data.id),
                "plan_id": command.plan_id,
                "visibility": command.visibility.value if command.visibility else None,
            },
        )
