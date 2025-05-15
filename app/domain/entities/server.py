from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.values.servers import ApiType, ProtocolType, Region


class CountryCode(Enum):
    RUSSIA = 'RU'
    VIETNAM = 'VN'
    THAILAND = 'TH'
    PHILIPPINES = 'PH'
    MALAYSIA = 'MY'
    SINGAPORE = 'SG'
    JAPAN = 'JP'
    SOUTH_KOREA = 'KR'
    HONG_KONG = 'HK'
    TAIWAN = 'TW'
    INDIA = 'IN'
    INDONESIA = 'ID'
    AMERICA = 'USA'
    GERMANY = 'DE'
    FRANCE = "FR"
    POLAND = "PL"
    ITALY = "IT"
    CANADA = "CA"
    BRAZIL = "BR"
    AUSTRALIA = "AU"
    SWITZERLAND = "CH"


@dataclass
class ProtocolConfig(AggregateRoot):
    config: dict[str, Any]
    protocol_type: ProtocolType


@dataclass
class Server(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    ip: str
    port: int
    domain: str | None
    limit: int
    region: Region
    free: int

    api_type: ApiType

    api_config: dict[str, Any]

    protocol_configs: dict[ProtocolType, ProtocolConfig] = field(default_factory=dict)

