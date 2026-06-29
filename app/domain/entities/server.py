from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import (
    Capacity,
    FeatureCode,
    Location,
    PanelCredentials,
    PanelEndpoint,
    PanelType,
    ProtocolCode,
)


@dataclass
class VPNServer(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)

    name: str
    capacity: Capacity

    panel_type: PanelType
    panel_endpoint: PanelEndpoint
    panel_credentials: PanelCredentials

    locations: set[Location] = field(default_factory=set)
    support_protocols: set[ProtocolCode] = field(default_factory=set)
    support_features: set[FeatureCode] = field(default_factory=set)

    is_active: bool = field(default=True)
    tags: list[str] = field(default_factory=list)

    def validate(self) -> None:
        pass


    def supports(
        self,
        protocols: set[ProtocolCode],
        features: set[FeatureCode],
    ) -> bool:
        return protocols <= self.support_protocols and features <= self.support_features

    @property
    def is_available(self) -> bool:
        return self.is_active and self.capacity.has_capacity

    def increment_clients(self) -> None:
        self.capacity = Capacity(
            max_client=self.capacity.max_client,
            free=self.capacity.free + 1
        )

    def decrement_clients(self) -> None:
        if self.capacity.free <= 0:
            raise

        self.capacity = Capacity(
            max_client=self.capacity.max_client,
            free=self.capacity.free - 1
        )

