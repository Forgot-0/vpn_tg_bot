from dataclasses import dataclass, field
from typing import Any, FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import PanelConfig, PanelCredits, PanelType, ProtocolCode
from app.domain.values.subscriptions import PlanFeatureCode


@dataclass
class VPNServer(AggregateRoot):
    id: UUID

    panel_type: PanelType
    panel_config: PanelConfig
    panel_credits: PanelCredits

    region_code: str
    is_active: bool = True

    supported_protocols: FrozenSet[ProtocolCode] = frozenset()
    supported_features: FrozenSet[PlanFeatureCode] = frozenset()

    protocols_config: dict[ProtocolCode, dict[str, Any]] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.id:
            raise ValueError("VPNServer id cannot be empty")
        if not self.region_code:
            raise ValueError("VPNServer region_code cannot be empty")

    def supports(self, protocols: FrozenSet[ProtocolCode]) -> bool:
        return protocols.issubset(self.supported_protocols)
