from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.exception.base import SubscriptionPendingException
from app.domain.services.utils import now_utc, replace
from app.domain.values.servers import ProtocolType, Region
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId


class SubscriptionStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"


@dataclass
class Subscription(AggregateRoot):
    id: SubscriptionId = field(default_factory=lambda: SubscriptionId(uuid4()), kw_only=True)
    duration: int
    start_date: datetime = field(default_factory=now_utc, kw_only=True)

    device_count: int

    server_id: UUID
    region: Region

    user_id: UserId

    status: SubscriptionStatus = field(default=SubscriptionStatus.PENDING, kw_only=True)
    protocol_types: list[ProtocolType]

    @staticmethod
    def create(
        user_id: UserId,
        region: Region,
        server_id: UUID,
        duration: int,
        device_count: int,
        protocol_types: list[ProtocolType],
    ) -> "Subscription":
        subscription =  Subscription(
            duration=duration,
            device_count=device_count,
            server_id=server_id,
            region=region,
            user_id=user_id,
            protocol_types=protocol_types
        )
        return subscription


    @property
    def end_date(self) -> datetime:
        return self.start_date + timedelta(days=self.duration)

    def is_active(self) -> bool:
        return now_utc() < replace(self.end_date)

    def activate(self) -> None:
        self.status = SubscriptionStatus.ACTIVE
        self.start_date = now_utc()

    def upgrade_devices(self, new_device_count: int) -> None:
        self.device_count = new_device_count

    def change_region(self, new_region: Region) -> None:
        self.region = new_region

    def renew(self, duration: int):
        if self.status  == SubscriptionStatus.PENDING:
            raise SubscriptionPendingException(subscription_id=self.id.as_generic_type())

        if replace(self.end_date) < now_utc():
            self.start_date = now_utc()
            self.duration = duration
        else:
            self.duration += duration
