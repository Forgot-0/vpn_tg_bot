from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.values.servers import ProtocolType, Region
from domain.values.subscriptions import SubscriptionId


@dataclass
class Subscription(AggregateRoot):
    id: SubscriptionId = field(default_factory=lambda: SubscriptionId(uuid4()), kw_only=True)
    duration: int
    start_date: datetime

    device_count: int

    server_id: UUID
    region: Region

    protocol_types: list[ProtocolType]

    @property
    def end_date(self) -> datetime:
        return self.start_date + timedelta(days=self.duration)

    def is_active(self) -> bool:
        return datetime.now() < self.start_date + timedelta(days=self.duration)

    def upgrade_devices(self, new_device_count: int):
        self.device_count = new_device_count

    def change_region(self, new_region: Region):
        self.region = new_region

    def calculate_price(self) -> int:
        return 3*self.device_count*self.duration*len(self.protocol_types)