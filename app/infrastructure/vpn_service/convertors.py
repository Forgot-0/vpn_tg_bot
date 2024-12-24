from datetime import datetime
from typing import Any

from application.dto.profile import Profile


def convert_profile_dict_to_dto(data: dict[str, Any]) -> Profile:
    return Profile(
        id=data['email'],
        download=data['down']/1024/1024/1024,
        upload=data['up']/1024/1024/1024,
        end_time=datetime.fromtimestamp(data['expiryTime']//1000),
        limit_trafic=data['total']/1024/1024/1024,
        vpn_url=data['vpn_url']
    )