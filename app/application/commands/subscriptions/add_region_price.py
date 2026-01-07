from dataclasses import dataclass

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.price import BasePriceRepository
from app.domain.values.servers import Region
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class AddRegionProceCommand(BaseCommand):
    region_code: str
    coef: float

    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class AddRegionProceCommandHandler(BaseCommandHandler[AddRegionProceCommand, None]):
    price_repository: BasePriceRepository
    role_access_control: RoleAccessControl

    async def handle(self, command: AddRegionProceCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        await self.price_repository.add_region(
            region=Region.region_by_code(command.region_code),
            coef=command.coef
        )