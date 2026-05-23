from dataclasses import dataclass
from typing import FrozenSet

from app.domain.values.servers import PanelConfig, PanelCredits, PanelType
from app.domain.values.subscriptions import PlanFeatureCode, VPNProtocol



@dataclass
class VPNServer:
    id: str

    panel_type: PanelType
    panel_config: PanelConfig
    panle_credits: PanelCredits

    region_code: str
    is_active: bool = True

    supported_protocols: FrozenSet[VPNProtocol] = frozenset()
    supported_features: FrozenSet[PlanFeatureCode] = frozenset()


    def supports(self, protocols: FrozenSet[VPNProtocol]) -> bool:
        return protocols.issubset(self.supported_protocols)

