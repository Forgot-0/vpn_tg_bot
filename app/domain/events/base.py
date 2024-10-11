from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import (
    UUID,
    uuid4,
)



@dataclass(frozen=True)
class BaseEvent(ABC):
    event_id: UUID = field(default_factory=uuid4, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
