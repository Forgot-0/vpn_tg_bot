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

    uri_login: str
    uri_create: str
    uri_delete: str
    uri_update: str
    uri_get: str