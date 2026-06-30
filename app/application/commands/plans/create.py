from dataclasses import dataclass, field
from decimal import Decimal
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.users import UserJWTData
from app.application.event_bus import EventBus
from app.domain.entities.plan import PricingRule, SubscriptionPlan
from app.domain.repositories.plans import PlanRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import PlanVisibility, SubscriptionLimits


logger = logging.getLogger(__name__)



@dataclass(frozen=True)
class MoneyAmount:

    amount: Decimal
    currency: str

    def to_money(self) -> Money:
        return Money(self.amount, self.currency)
 
 
@dataclass(frozen=True)
class CreatePlanCommand(BaseCommand):
    user_jwt_data: UserJWTData

    code: str
    name: str
    description: str


    strategy: str
    reset_every_n_days: int | None = None
    custom_cron: str | None = None

    visibility: PlanVisibility = PlanVisibility.PUBLIC
    order_index: int = 0
    is_trial: bool = False
    is_active: bool = True

    duration_days: int | None = None
    traffic_limit_gb: float | None = None
    max_devices: int | None = None
    features: set[str] = field(default_factory=set)
    protocols: set[str] = field(default_factory=set)
    prices: list[MoneyAmount] = field(default_factory=list)

    price_per_day: MoneyAmount | None = None
    price_per_gb: MoneyAmount | None = None
    price_per_device: MoneyAmount | None = None
    feature_surcharges: dict[FeatureCode, Decimal] = field(default_factory=dict)
    protocol_surcharges: dict[ProtocolCode, Decimal] = field(default_factory=dict)
    allowed_durations: list[int] = field(default_factory=list)
    allowed_traffic_gb: list[float] = field(default_factory=list)
    allowed_features: set[FeatureCode] = field(default_factory=set)
    allowed_protocols: set[ProtocolCode] = field(default_factory=set)
    max_devices_limit: int | None = None

    @property
    def is_fixed_request(self) -> bool:
        return (
            self.duration_days is not None or
            len(self.prices) != 0 or self.traffic_limit_gb is not None or
            self.max_devices is not None
        )

    @property
    def is_dynamic_request(self) -> bool:
        return (
            self.price_per_day is not None or
            self.price_per_gb is not None or
            self.price_per_device is not None
        )


@dataclass(frozen=True)
class CreatePlanCommandHandler(BaseCommandHandler[CreatePlanCommand, None]):
    plan_repository: PlanRepository
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: CreatePlanCommand) -> None:
        plan = await self.plan_repository.get_by_code(command.code)
        if plan is not None:
            raise

        if command.is_fixed_request:
            plan = SubscriptionPlan.create_fixed(
                code=command.code,
                name=command.name,
                description=command.description,
                limit=SubscriptionLimits.create(
                    duration_days=command.duration_days,
                    trafic_bytes_limit=int(command.traffic_limit_gb * 1024**3) if command.traffic_limit_gb else None,
                    max_devices=command.max_devices,
                    features=command.features,
                    protocols=command.protocols,
                    strategy=command.strategy,
                    reset_every_n_days=command.reset_every_n_days,
                    custom_cron=command.custom_cron,
                ),
                prices={Money(m.amount, m.currency) for m in command.prices}
            )
        else:
            assert command.price_per_day is not None
            assert command.price_per_gb is not None
            assert command.price_per_device is not None
            currency = command.price_per_day.currency

            feature_surcharges = {
                feature: Money(amount, currency)
                for feature, amount in command.feature_surcharges.items()
            }

            protocol_surcharges = {
                protocol: Money(amount, currency)
                for protocol, amount in command.protocol_surcharges.items()
            }
    
            plan = SubscriptionPlan.create_dynamic(
                code=command.code,
                name=command.name,
                description=command.description,
                price_rule=PricingRule(
                    price_per_day=command.price_per_day.to_money(),
                    price_per_gb=command.price_per_gb.to_money(),
                    price_per_device=command.price_per_device.to_money(),
                    feature_surcharges=feature_surcharges,
                    protocol_surcharges=protocol_surcharges,
                ),
                allowed_durations=list(command.allowed_durations),
                allowed_traffic_gb=list(command.allowed_traffic_gb),
                allowed_features=set(command.allowed_features),
                allowed_protocols=set(command.allowed_protocols),
                max_devices_limit=command.max_devices_limit,
            )

        plan.visibility = command.visibility
        plan.order_index = command.order_index
        plan.is_trial = command.is_trial
        plan.is_active = command.is_active
 
        await self.plan_repository.add(plan)
        await self.uow.commit()
        logger.info(
            "Created plan", extra={
                "created_by": str(command.user_jwt_data.id),
                "plan_code": command.code
            }
        )
