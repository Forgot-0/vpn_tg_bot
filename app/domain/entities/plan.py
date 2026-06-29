from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import PlanVisibility, SubscriptionLimits




@dataclass
class PricingRule:
    price_per_day: Money
    price_per_gb: Money
    price_per_device: Money

    feature_surcharges: dict[FeatureCode, Money] = field(default_factory=dict)
    protocol_surcharges: dict[ProtocolCode, Money] = field(default_factory=dict)


@dataclass
class SubscriptionPlan(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)

    code: str
    name: str
    description: str

    limit: SubscriptionLimits
    price: set[Money] = field(default_factory=set)
    price_rule: PricingRule | None = field(default=None)

    visibility: PlanVisibility = field(default=PlanVisibility.PUBLIC)
    order_index: int = field(default=0)
    is_trial: bool = field(default=False)

    def validate(self) -> None:
        ...

