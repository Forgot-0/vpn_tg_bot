from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.values.servers import ProtocolType, Region
from domain.values.subscriptions import SubscriptionId
from domain.values.users import UserId


class SubscriptionStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"

@dataclass
class Subscription(AggregateRoot):
    id: SubscriptionId = field(default_factory=lambda: SubscriptionId(uuid4()), kw_only=True)
    duration: int
    start_date: datetime = field(default_factory=datetime.now, kw_only=True)

    device_count: int

    server_id: UUID
    region: Region

    user_id: UserId

    status: SubscriptionStatus = field(default=SubscriptionStatus.PENDING, kw_only=True)
    protocol_types: list[ProtocolType]

    @property
    def end_date(self) -> datetime:
        return self.start_date + timedelta(days=self.duration)

    def is_active(self) -> bool:
        return datetime.now() < self.start_date + timedelta(days=self.duration)

    def activate(self) -> None:
        self.status = SubscriptionStatus.ACTIVE

    def upgrade_devices(self, new_device_count: int):
        if self.status in (SubscriptionStatus.EXPIRED, SubscriptionStatus.PENDING):
            raise

        self.device_count = new_device_count

    def change_region(self, new_region: Region):
        if self.status in (SubscriptionStatus.EXPIRED, SubscriptionStatus.PENDING):
            raise

        self.region = new_region

    def renew(self, duration: int):
        if self.status  == SubscriptionStatus.PENDING:
            raise

        if self.end_date < datetime.now():
            self.start_date = datetime.now()
            self.duration = duration
        else:
            self.duration += duration
