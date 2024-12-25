from dataclasses import dataclass
from datetime import datetime
from typing import Any

from application.dto.base import BaseDTO


@dataclass
class ProfileDTO(BaseDTO):
    id: str
    download: int
    upload: int

    end_time: datetime
    limit_trafic: int
    vpn_url: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ProfileDTO':
        return ProfileDTO(
            id=data['email'],
            download=data['down']/1024/1024/1024,
            upload=data['up']/1024/1024/1024,
            end_time=datetime.fromtimestamp(data['expiryTime']//1000),
            limit_trafic=data['total']/1024/1024/1024,
            vpn_url=data['vpn_url']
        )