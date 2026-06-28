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
    ProtocolCode
)


@dataclass
class VPNServer(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)

    name: str
    capacity: Capacity

    panel_type: PanelType
    panel_endpoint: PanelEndpoint
    panel_creditials: PanelCredentials

    locations: set[Location] = field(default_factory=set)
    support_protocols: set[ProtocolCode] = field(default_factory=set)
    feature_protocols: set[FeatureCode] = field(default_factory=set)


    def validate(self) -> None:
        ...


