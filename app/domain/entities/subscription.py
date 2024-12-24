from dataclasses import dataclass, field
from datetime import timedelta
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot



@dataclass
class Subscription(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    name: str
    description: str
    limit_ip: int = field(default=1, kw_only=True)
    limit_trafic: int = field(default=0, kw_only=True)
    duration: timedelta = field(default_factory=timedelta, kw_only=True)
    price: float
    is_active: bool = field(default=True, kw_only=True)


