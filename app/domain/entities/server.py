from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot




class Country(Enum):
    RU = 'RU'
    NL = 'NL'
    AMERICA = 'USA'
    GERMANY = 'DE'


@dataclass
class Server(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
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

    def get_by_id(self, id: str) -> str:
        return f"http://{self.ip}:{self.panel_port}/{self.panel_path}/panel/api/inbounds/getClientTrafficsById/{id}"

    def update_by_id(self, id: str) -> str:
        return f"http://{self.ip}:{self.panel_port}/{self.panel_path}/panel/api/inbounds/updateClient/{id}"