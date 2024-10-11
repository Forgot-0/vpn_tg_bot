import asyncio
from dataclasses import dataclass, field
from json import dump, dumps, loads
from aiohttp import ClientSession, FormData
import requests

from datetime import datetime, timedelta

print(datetime.now().timestamp())

1728646782
1728732747108
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
#     json={
#         'id': 1,
#         'settings': dumps({
#             "clients": [
#                 {
#                     "id": "0638e561-4144-4520-a144-1a8fa81e01e2",
#                     "flow": "xtls-rprx-vision",
#                     "email": "gewg",
#                     "expiryTime": 1730374666807,
#                     "enable": True,
#                 }
#             ]
#         })
#     }
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


async def main():
    
    # new_data = data.model_dump_json()
    # print(new_data)
    # new_data['settings'] = dumps(new_data['settings'])
    s = ClientSession()
        
    # resp1 = await s.post(url=url+"login", data={
    #     'username': 'Forgot',
    #     'password': 'Frog2005',
    #     'loginSecret': '8rjmOssitQLHcne5LvfWH3FR1jOo1LPUfcACFooYJt3dgaytkaVIohJLLYvOlXuP'
    # })
    # print(await resp1.text())
    # print(resp1.status)
    # resp = await s.post(url=url+'panel/inbound/addClient', json=new_data, cookies=resp1.cookies)
    # print(resp.status)
    # responce = ( await resp.json())
    # print(responce['success'])

    # await s.close()

# asyncio.run(main())


print(dumps({
        'ip': '80.85.247.3',
        'port': '55801',
        'domain': 'server.domain',
        'limit': 10,
        'pbk': 'eA7IiJg2phKsbJLqVT6Yr3bEp69-L4qiU3tM1Dw7LWo',
        'country': 'nl',
        'free': 3,

        'uri_login': 'http://80.85.247.3:55801/safsdfsadfa/login',
        'uri_create': 'http://80.85.247.3:55801/safsdfsadfa/panel/inbound/addClient',
        'uri_delete': 'server.uri_delete',
        'uri_update': 'server.uri_update',
        'uri_get': 'server.uri_get'
    })
)
{"ip": "80.85.247.3", "port": "55801", "domain": "server.domain", "limit": 10, "pbk": "eA7IiJg2phKsbJLqVT6Yr3bEp69-L4qiU3tM1Dw7LWo", "country": "nl", "free": 3, "uri_login": "http://80.85.247.3:55801/safsdfsadfa/login", "uri_create": "http://80.85.247.3:55801/safsdfsadfa/panel/inbound/addClient", "uri_delete": "server.uri_delete", "uri_update": "server.uri_update", "uri_get": "server.uri_get"}