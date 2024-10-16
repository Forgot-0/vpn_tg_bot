from dataclasses import dataclass, field
from enum import Enum

from domain.entities.base import AggregateRoot




class Country(Enum):
    RU = 'ru'
    NL = 'nl'
    AMERICA = 'USA'
    Germany = 'DE'


@dataclass
class Server(AggregateRoot):
    ip: str
    port: int
    domain: str
    limit: int
    pbk: str
    country: Country
    free: int

    name: str
    panel_port: int
    panel_path: str

    @property
    def url_login(self) -> str:
        return f'http://{self.ip}:{self.panel_port}/{self.panel_path}/login'
    @property
    def url_create(self) -> str:
        return f"http://{self.ip}:{self.panel_port}/{self.panel_path}/panel/api/inbounds/addClient"

    @property
    def url_delete_not_active(self) -> str:
        return f"http://{self.ip}:{self.panel_port}/{self.panel_path}/panel/api/inbounds/delDepletedClients/-1"

    @property
    def url_list(self) -> str:
        return f"http://{self.ip}:{self.panel_port}/{self.panel_path}/panel/api/inbounds/list"

