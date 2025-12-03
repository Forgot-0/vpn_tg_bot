
from dataclasses import dataclass, field
from typing import Type
from app.domain.services.ports import BaseApiClient
from app.domain.values.servers import ApiType


@dataclass
class ApiClientFactory:
    _registry: dict[ApiType, BaseApiClient] = field(default_factory=dict)

    def register(self, api_type: ApiType, api_client: BaseApiClient) -> None:
        self._registry[api_type] = api_client

    def get(self, api_type: ApiType) -> BaseApiClient:
        return self._registry[api_type]
