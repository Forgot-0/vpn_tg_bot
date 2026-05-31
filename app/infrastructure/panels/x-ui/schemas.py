from typing import Any, Literal

from pydantic import BaseModel



class Option(BaseModel):
    id: int
    remark: str
    protocol: Literal["vless", "vmess"]
    port: int
    tlsFlowCapable: bool
    


class InbounOptions(BaseModel):
    # /panel/api/inbounds/options
    success: bool
    obj: list[Option]


class SeverSubscriptionSettings(BaseModel):
    subEnable: bool
    subPort: int
    subPath: str
    subDomain: str
    subCertFile: str

"""
{
  "client": {
    "email": "pqdcqpwv5",
    "subId": "jiq4y71rtts12uyo",
    "id": "0423013b-7cb1-4343-91e0-8ede5518b0bc",
    "password": "fpccjbvzpzissnhj",
    "auth": "gtvaebwlux8joq79",
    "flow": "xtls-rprx-vision",
    "totalGB": 13958643712,
    "expiryTime": 0,
    "limitIp": 3,
    "tgId": 0,
    "comment": "",
    "enable": true,
    "reverse": {
      "tag": "sagsfd"
    }
  },
  "inboundIds": [
    1
  ]
}
"""
class ServerInboundSettings:
    id: int
    protocol: str
    streamSettings: dict[str, Any]


class ServerSettings(BaseModel):
    inbounds: dict[int, str]
    subscription: SeverSubscriptionSettings

