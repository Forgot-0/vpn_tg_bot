
from dataclasses import dataclass
from typing import Type
from domain.services.ports import BaseApiClient
from domain.values.servers import ApiType


@dataclass
class ApiClientFactory:
    _registy: dict[ApiType, BaseApiClient]

    def registy(self, api_type: ApiType, api_client: BaseApiClient) -> None:
        self._registy[api_type] = api_client

    def get(self, api_type: ApiType) -> BaseApiClient:
        return self._registy[api_type]
