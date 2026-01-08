from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.price import BasePriceRepository
from app.domain.values.servers import Region
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddRegionPriceCommand(BaseCommand):
    region_code: str
    coef: float

    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class AddRegionPriceCommandHandler(BaseCommandHandler[AddRegionPriceCommand, None]):
    price_repository: BasePriceRepository
    role_access_control: RoleAccessControl

    async def handle(self, command: AddRegionPriceCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        await self.price_repository.add_region(
            region=Region.region_by_code(command.region_code),
            coef=command.coef
        )

        logger.info(
            "Add region to price config",
            extra={
                "user_by": command.user_jwt_data.id,
                "region_code": command.region_code,
                "coef": command.coef
            }
        )