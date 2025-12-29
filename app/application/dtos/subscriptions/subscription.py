from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import ProtocolType


@dataclass
class SubscriptionDTO(BaseDTO):
    id: UUID
    duration: int
    start_date: datetime
    device_count: int
    flag: str
    name: str
    code: str
    status: str
    protocol_types: list[ProtocolType]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'SubscriptionDTO':
        return SubscriptionDTO(
            id=UUID(data['id']) if isinstance(data['id'], str) else data['id'],
            duration=data['duration'],
            start_date=data['start_date'],
            device_count=data['device_count'],
            flag=data['flag'],
            name=data['name'],
            code=data['code'],
            status=data['status'],
            protocol_types=data['protocol_types'],
        )

    @classmethod
    def from_entity(cls, entity: Subscription) -> 'SubscriptionDTO':
        return SubscriptionDTO(
            id=entity.id.value,
            duration=entity.duration,
            start_date=entity.start_date,
            device_count=entity.device_count,
            flag=entity.region.flag,
            name=entity.region.name,
            code=entity.region.code,
            status=entity.status.value,
            protocol_types=entity.protocol_types
        )


