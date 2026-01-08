from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.entities.price import PriceConfig
from app.domain.repositories.price import BasePriceRepository
from app.domain.values.servers import ProtocolType, Region
from app.domain.values.users import UserRole


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class UpdatePriceConfigCommand(BaseCommand):
    daily_rate: float
    device_rate_multiplier: float
    region_base_multiplier: float
    region_multipliers: dict[str, float]
    protocol_base_multiplier: float
    protocol_multipliers: dict[str, float]

    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class UpdatePriceConfigCommandHandler(BaseCommandHandler[UpdatePriceConfigCommand, None]):
    price_repository: BasePriceRepository
    role_access_control: RoleAccessControl

    async def handle(self, command: UpdatePriceConfigCommand) -> None:
        if not self.role_access_control.can_action(
            UserRole(command.user_jwt_data.role), target_role=UserRole.ADMIN
        ):
            raise ForbiddenException()

        cfg = PriceConfig(
            daily_rate=command.daily_rate,
            device_rate_multiplier=command.device_rate_multiplier,
            region_base_multiplier=command.region_base_multiplier,
            region_multipliers={
                Region.region_by_code(code): command.region_multipliers[code]
                for code in command.region_multipliers
            },
            protocol_base_multiplier=command.protocol_base_multiplier,
            protocol_multipliers={
                ProtocolType(protocol): command.protocol_multipliers[protocol]
                for protocol in command.protocol_multipliers
            }
        )

        await self.price_repository.update(cfg=cfg)
        logger.info(
            "Update price config",
            extra={
                "user_by": command.user_jwt_data.id,
                "new_cfg": cfg
            }
        )