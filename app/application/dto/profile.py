from dataclasses import dataclass
from datetime import datetime


@dataclass
class Profile:
    id: str
    download: int
    upload: int

    end_time: datetime
    limit_trafic: int
    vpn_url: str