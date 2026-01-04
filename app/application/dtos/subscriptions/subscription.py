from dataclasses import dataclass
from datetime import datetime
from typing import Any
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
    user_id: UUID
    server_id: UUID
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
            user_id=data['user_id'],
            server_id=data['server_id'],
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
            user_id=entity.user_id.value,
            server_id=entity.server_id,
            flag=entity.region.flag,
            name=entity.region.name,
            code=entity.region.code,
            status=entity.status.value,
            protocol_types=entity.protocol_types
        )

