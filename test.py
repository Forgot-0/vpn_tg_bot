import asyncio
from dataclasses import dataclass, field
from enum import Enum
from json import dump, dumps, loads
from aiohttp import ClientSession, FormData
import requests

from datetime import datetime, timedelta

requests.post('https://7cd6-80-85-247-3.ngrok-free.app/webhook',json={}, verify=False, cert=False)

# url = "http://80.85.247.3:55801/safsdfsadfa/"

# session = requests.Session()

# log = session.post(
#     url="http://80.85.247.3:55801/safsdfsadfa/login", 
#     data={
#         'username': 'Forgot',
#         'password': 'Frog2005',
#         'loginSecret': '8rjmOssitQLHcne5LvfWH3FR1jOo1LPUfcACFooYJt3dgaytkaVIohJLLYvOlXuP'
#         }
#     )

# print(log.content)
# cl = session.get(url=url+'panel/api/inbounds/getClientTrafficsById/f6bfa6ab-aa6d-4710-b448-e21053ccd490')
# print(cl.content)
# session.close()

# create = session.post(
#     url=url+'panel/inbound/addClient',
    # json={
    #     'id': 1,
    #     'settings': dumps({
    #         "clients": [
    #             {
    #                 "id": "0638e561-4144-4520-a144-1a8fa81e01e2",
    #                 "flow": "xtls-rprx-vision",
    #                 "email": "gewg",
    #                 "expiryTime": 1730374666807,
    #                 "enable": True,
    #             }
    #         ]
    #     })
    # }
#     )

# print(log.text)
# print(create.content)


from uuid import UUID
from pydantic import BaseModel, Field, JsonValue


# json={
#         'id': 1,
#         'settings': dumps({
#             "clients": [
#                 {
#                     "id": UUID("0638e561-4144-4520-a144-1a8fa81e01e2"),
#                     "flow": "xtls-rprx-vision",
#                     "email": "gewg",
#                     "limitIp": 0,
#                     "totalGB": 0,
#                     "expiryTime": 1730374666807,
#                     "enable": True,
#                     "tgId": "",
#                     "subId": "fdfx4qkzdnvgthmu",
#                     "reset": 0
#                 }
#             ]
#         })
#     }

# print(json)
# class Client(BaseModel):
#     id: str
#     flow: str = "xtls-rprx-vision"
#     email: str
#     limitIp: int
#     totalGB: int
#     expiryTime: int
#     enable: bool = True
#     tgId: str
#     subId: str
#     reset: int = 0


# class Settings(BaseModel):
#     clients: list[Client]


# class CreateVpnUrl(BaseModel):
#     id: int = Field(default=1)
#     settings: Settings


# data = CreateVpnUrl(**json)
# print(data.model_dump())


# reate = session.post(
#     url=url+'panel/inbound/addClient',
#     json=data.model_dump_json()
#     )
# print(reate.content)



# print(dumps({
#         'ip': '80.85.247.3',
#         'port': '55801',
#         'domain': 'server.domain',
#         'limit': 10,
#         'pbk': 'eA7IiJg2phKsbJLqVT6Yr3bEp69-L4qiU3tM1Dw7LWo',
#         'country': 'nl',
#         'free': 3,

#         'uri_login': 'http://80.85.247.3:55801/safsdfsadfa/login',
#         'uri_create': 'http://80.85.247.3:55801/safsdfsadfa/panel/inbound/addClient',
#         'uri_delete': 'server.uri_delete',
#         'uri_update': 'server.uri_update',
#         'uri_get': 'server.uri_get'
#     })
# )
# {"ip": "80.85.247.3", "name":"VLESS%20%D1%81%20XTLS-Reality", "port": "443", "domain": "server.domain", "limit": 10, "pbk": "eA7IiJg2phKsbJLqVT6Yr3bEp69-L4qiU3tM1Dw7LWo", "country": "nl", "free": 3, "uri_login": "http://80.85.247.3:55801/safsdfsadfa/login", "uri_create": "http://80.85.247.3:55801/safsdfsadfa/panel/inbound/addClient", "uri_delete": "server.uri_delete", "uri_update": "server.uri_update", "uri_get": "server.uri_get"}


# {
#     'file_id': 'AgACAgIAAxkBAANfZwvqYrWKjJPA3DeM7Sn726fpaZEAAqDjMRuyMWFImJPCTo12u2gBAAMCAANzAAM2BA', 
#     'file_unique_id': 'AQADoOMxG7IxYUh4', 'width': 90, 'height': 39, 'file_size': 1027}, 

print(dumps({
    "rules": [
        {
            "domain_suffix": [
                ".ru"
            ],
            "outbound": "direct"
        }
    ]
}
))