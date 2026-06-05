from __future__ import annotations

from typing import Any

from app.domain.entities.server import PanelConnection
from app.domain.values.servers import PanelCredentials, PanelEndpoint, PanelType
from app.infrastructure.db.models.server_topology import PanelConnectionModel


class PanelConnectionMapper:
    @staticmethod
    def _endpoint_from_json(raw: dict[str, Any]) -> PanelEndpoint:
        return PanelEndpoint(
            host=raw["host"],
            port=int(raw["port"]),
            path=raw.get("path", "/"),
            use_ssl=raw.get("use_ssl", True),
        )

    @staticmethod
    def _endpoint_to_json(endpoint: PanelEndpoint) -> dict[str, Any]:
        return {
            "host": endpoint.host,
            "port": endpoint.port,
            "path": endpoint.path,
            "use_ssl": endpoint.use_ssl,
        }

    @staticmethod
    def _credentials_from_json(raw: dict[str, Any]) -> PanelCredentials:
        return PanelCredentials(
            username=raw.get("username"),
            password=raw.get("password"),
            api_token=raw.get("api_token"),
        )

    @staticmethod
    def _credentials_to_json(creds: PanelCredentials) -> dict[str, Any]:
        return {
            "username": creds.username,
            "password": creds.password,
            "api_token": creds.api_token,
        }

    @classmethod
    def to_entity(cls, model: PanelConnectionModel) -> PanelConnection:
        return PanelConnection(
            id=model.id,
            name=model.name,
            panel_type=PanelType(model.panel_type),
            endpoint=cls._endpoint_from_json(model.endpoint),
            credentials=cls._credentials_from_json(model.credentials_encrypted),
            config=model.config or {},
            is_active=model.is_active,
        )

    @classmethod
    def to_model(cls, entity: PanelConnection) -> PanelConnectionModel:
        return PanelConnectionModel(
            id=entity.id,
            name=entity.name,
            panel_type=entity.panel_type.value,
            endpoint=cls._endpoint_to_json(entity.endpoint),
            credentials_encrypted=cls._credentials_to_json(entity.credentials),
            config=entity.config,
            is_active=entity.is_active,
        )

    @classmethod
    def update_model(cls, model: PanelConnectionModel, entity: PanelConnection) -> None:
        model.name = entity.name
        model.panel_type = entity.panel_type.value
        model.endpoint = cls._endpoint_to_json(entity.endpoint)
        model.credentials_encrypted = cls._credentials_to_json(entity.credentials)
        model.config = entity.config
        model.is_active = entity.is_active
