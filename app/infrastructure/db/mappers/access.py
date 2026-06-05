from __future__ import annotations

from decimal import Decimal

from app.domain.entities.access import ProvisionedAccess
from app.domain.values.servers import PanelType, ProtocolCode
from app.domain.values.subscriptions import AccessCredential, AccessFormat, ProvisioningStatus, RemoteAccessState
from app.infrastructure.db.models.access import ProvisionedAccessModel


class ProvisionedAccessMapper:
    @staticmethod
    def _credentials_to_json(credentials: list[AccessCredential]) -> list[dict]:
        return [
            {
                "format": credential.format.value,
                "value": credential.value,
                "protocol": credential.protocol.value if credential.protocol else None,
                "panel_client_id": credential.panel_client_id,
                "label": credential.label,
            }
            for credential in credentials
        ]

    @staticmethod
    def _credentials_from_json(raw: list[dict]) -> list[AccessCredential]:
        return [
            AccessCredential(
                format=AccessFormat(item["format"]),
                value=item["value"],
                protocol=ProtocolCode(item["protocol"]) if item.get("protocol") else None,
                panel_client_id=item.get("panel_client_id"),
                label=item.get("label", ""),
            )
            for item in raw
        ]

    @classmethod
    def to_entity(cls, model: ProvisionedAccessModel) -> ProvisionedAccess:
        return ProvisionedAccess(
            id=model.id,
            subscription_id=model.subscription_id,
            server_id=model.server_id,
            panel_type=PanelType(model.panel_type),
            panel_client_id=model.panel_client_id,
            inbound_ids=tuple(int(item) for item in model.inbound_ids),
            credentials=cls._credentials_from_json(model.credentials),
            status=ProvisioningStatus(model.status),
            remote_state=RemoteAccessState(model.remote_state),
            used_traffic_gb=Decimal(model.used_traffic_gb),
            last_synced_at=model.last_synced_at,
            last_error=model.last_error,
            metadata=model.meta,
        )

    @classmethod
    def to_model(cls, entity: ProvisionedAccess) -> ProvisionedAccessModel:
        return ProvisionedAccessModel(
            id=entity.id,
            subscription_id=entity.subscription_id,
            server_id=entity.server_id,
            panel_type=entity.panel_type.value,
            panel_client_id=entity.panel_client_id,
            inbound_ids=[str(item) for item in entity.inbound_ids],
            credentials=cls._credentials_to_json(entity.credentials),
            status=entity.status.value,
            remote_state=entity.remote_state.value,
            used_traffic_gb=entity.used_traffic_gb,
            last_synced_at=entity.last_synced_at,
            last_error=entity.last_error,
            meta=entity.metadata,
        )
