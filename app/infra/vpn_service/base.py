from abc import ABC, abstractmethod
from dataclasses import dataclass

from infra.vpn_service.schema import Client, CreateVpnUrl



@dataclass(kw_only=True)
class BaseVpnService(ABC):
    main_url: str
    ip: str
    pbk: str
    username: str
    password: str
    secret: str

    urn_login: str
    urn_create: str
    urn_update: str
    urn_delete: str
    urn_get: str

    @abstractmethod
    async def create(self, data: CreateVpnUrl) -> str:
        ...

    @abstractmethod
    async def udate(self, data: Client) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: str) -> Client:
        ...

    @abstractmethod
    async def login(self) -> None:
        ...

    @abstractmethod
    def get_vpn_urn(self, data: CreateVpnUrl) -> str:
        ...

    @property
    def url(self) -> str:
        return f'http://{self.main_url}'

    @property
    def uri_create(self) -> str:
        return f'{self.url}/{self.urn_create}'

    @property
    def uri_delete(self) -> str:
        return f'{self.url}/{self.urn_delete}'

    @property
    def uri_update(self) -> str:
        return f'{self.url}/{self.urn_update}'

    @property
    def uri_get(self) -> str:
        return f'{self.url}/{self.urn_get}'

    @property
    def uri_login(self) -> str:
        return f'{self.url}/{self.urn_login}'