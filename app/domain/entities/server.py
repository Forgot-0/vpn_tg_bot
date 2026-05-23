from dataclasses import dataclass
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import PanelConfig, PanelCredits, PanelType
from app.domain.values.subscriptions import PlanFeatureCode, VPNProtocol


@dataclass
class VPNServer(AggregateRoot):
    id: UUID

    panel_type: PanelType
    panel_config: PanelConfig
    panel_credits: PanelCredits

    region_code: str
    is_active: bool = True

    supported_protocols: FrozenSet[VPNProtocol] = frozenset()
    supported_features: FrozenSet[PlanFeatureCode] = frozenset()

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.id:
            raise ValueError("VPNServer id cannot be empty")
        if not self.region_code:
            raise ValueError("VPNServer region_code cannot be empty")

    def supports(self, protocols: FrozenSet[VPNProtocol]) -> bool:
        return protocols.issubset(self.supported_protocols)
