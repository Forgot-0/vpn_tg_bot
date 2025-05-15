from enum import Enum
from uuid import uuid4
import json

class ProtocolType(Enum):
    vless = "VLESS"
    mock = "MOCK"

print(json.dumps({
    "_id": uuid4().hex,
    "ip": "80.85.247.3",
    "port": 55801,
    "domain": "",
    "limit": 100,
    "region": "test",
    "free": "test",
    "api_type": "3X-UI",
    "api_config": {},
    "protocol_configs": {
        ProtocolType.vless.name: {
            "config": {},
            "protocol_type": ProtocolType.vless.name
        }
    }
}))