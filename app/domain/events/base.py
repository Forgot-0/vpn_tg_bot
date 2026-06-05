from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.services.clock import now_utc


@dataclass(frozen=True)
class DomainEvent(ABC):
    event_id: UUID = field(default_factory=uuid4, kw_only=True)
    occurred_at: datetime = field(default_factory=now_utc, kw_only=True)

    @classmethod
    def event_name(cls) -> str:
        name = getattr(cls, "__event_name__", None)
        if not name:
            raise AttributeError(f"{cls.__name__} must define __event_name__")
        return name