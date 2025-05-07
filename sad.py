# uri_login: 'http://80.85.247.3:55801/safsdfsadfa/login',
# uri_create: 'http://80.85.247.3:55801/safsdfsadfa/panel/inbound/addClient',

# http://{server.id}:{server.port_panel}/{server.panel_path}/panel/api/inbounds/{create}
# http://{server.id}:{server.port_panel}/{server.panel_path}/login
# http://{server.id}:{server.port_panel}/{server.panel_path}/panel/api/inbounds/addClient
# http://{server.id}:{server.port_panel}/{server.panel_path}/panel/api/inbounds/delDepletedClients/-1
# http://{server.id}:{server.port_panel}/{server.panel_path}/panel/api/inbounds/list


import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import wraps
from json import dumps, load, loads
from typing import Any
from uuid import UUID, uuid4

from aiogram import Bot


# json = {
#     'ip': '213.176.92.91',
#     'port': '443',
#     'domain': 'server.domain',
#     'limit': 30,
#     'pbk': 'KxbLR2xYdvIJY-lSnfKjNMKItCnbOCg5A3KUOoRKlDs',
#     'country': 'SE',
#     'free': 150,
#     'name': '',
#     'panel_port': 55801,
#     'panel_path': 'safsdfsadfa'
# }
# print(dumps(json))


# json = {
#     'type': 'notification', 
#     'event': 'payment.succeeded', 
#     'object': {
#         'id': '2ea104e8-000f-5000-a000-124d4aea937c', 
#         'status': 'succeeded', 
#         'amount': {
#             'value': '10.00', 
#             'currency': 'RUB'
#             }, 
#         'income_amount': {
#             'value': '9.65', 
#             'currency': 'RUB'
#             },
#         'description': 'Заказ №72', 
#         'recipient': {
#             'account_id': '473072', 
#             'gateway_id': '2325943'
#             }, 
#         'payment_method': {
#             'type': 'bank_card', 
#             'id': '2ea104e8-000f-5000-a000-124d4aea937c', 
#             'saved': False, 
#             'title': 'Bank card *4364', 
#             'card': {
#                 'first6': '220070', 
#                 'last4': '4364', 
#                 'expiry_year': '2033', 
#                 'expiry_month': '10', 
#                 'card_type': 'Mir', 
#                 'card_product': {
#                     'code': 'MSA', 
#                     'name': 'Mir Supreme'
#                     },
#                 'issuer_country': 'RU', 
#                 'issuer_name': 'T-Bank (Tinkoff)'
#                 }
#             }, 
#         'captured_at': '2024-10-15T22:48:27.762Z', 
#         'created_at': '2024-10-15T22:48:08.421Z', 
#         'test': False, 
#         'refunded_amount': {
#             'value': '0.00', 
#             'currency': 'RUB'
#             }, 
#         'paid': True, 
#         'refundable': True, 
#         'metadata': {
#             'tg_id': '1770295162', 
#             'cms_name': 'yookassa_sdk_python'
#             }, 
#         'authorization_details': {
#             'rrn': '428922038156', 
#             'auth_code': '090379', 
#             'three_d_secure': {
#                 'applied': True, 
#                 'protocol': 'v2', 
#                 'method_completed': True, 
#                 'challenge_completed': True
#                 }
#             }
#         }
#     }
# import requests
# # http://80.85.247.3:55801/safsdfsadfa/panel/api/inbounds/list
# cook = requests.post(
#     url='http://213.176.92.91:55801/safsdfsadfa/panel/login',
#     data={
#         'username': 'Forgot',
#         'password': 'Frog2005',
#         'loginSecret': '8rjmOssitQLHcne5LvfWH3FR1jOo1LPUfcACFooYJt3dgaytkaVIohJLLYvOlXuP'
#     }
# )

# res = requests.get(
#     url="http://213.176.92.91:55801/safsdfsadfa/panel/api/inbounds/getClientTrafficsById/3e34db6c-86b0-4696-ab0c-bd4943ad3be5",
#     cookies=cook.cookies

# )
# print(res.json())
# {
#     'id': '2ea1bb7d-000f-5000-8000-19d4976302c2', 
#     'status': 'pending', 
#     'amount': {
#         'value': '1.00', 
#         'currency': 'RUB'
#     },
#     'description': 'Заказ №72',
#     'recipient': {
#         'account_id': '473072', 
#         'gateway_id': '2325943'
#     },
#     'payment_method': {
#         'type': 'bank_card',
#         'id': '2ea1bb7d-000f-5000-8000-19d4976302c2',
#         'saved': False
#     },
#     'created_at': '2024-10-16T11:47:09.111Z',
#     'confirmation': {
#         'type': 'redirect',
#         'return_url': 'https://t.me/forgot_vpn_bot',
#         'confirmation_url': 'https://yoomoney.ru/checkout/payments/v2/contract?orderId=2ea1bb7d-000f-5000-8000-19d4976302c2'
#     },
#     'test': False,
#     'paid': False,
#     'refundable': False,
#     'metadata': {
#         'subscription_id': '4bfb3224-8a73-4934-ad47-44db8ad21511', 
#         'tg_id': '1770295162'
#     }
# }


# certbot certonly --webroot --webroot-path=/var/www/certbot \
#   --email welcome2038@gmail.com --agree-tos --no-eff-email \
#   -d my-backend-test.ru

# .PHONY: certbot
# certbot:
# 	${DC} -f ${WEB_SERVER} -f ${BOT_APP} ${ENV} run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d my-backend-test.ru
# docker network create shared_network
# docker-compose -f docker_compose/webserver.yaml -f docker_compose/storage.yaml -f docker_compose/app.yaml up -d --build
# export $(grep -v '^#' .env | xargs)
# echo "DATABASE_USERNAME: $DATABASE_USERNAME"
# chmod 644 .env
# docker ps -a
# 
# git clone https://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@github.com/Forgot-0/vpn_tg_bot.git
# sudo apt update
# sudo apt install apt-transport-https ca-certificates curl software-properties-common
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# sudo apt update
# sudo apt install docker-ce
# sudo systemctl status docker
# sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose
# docker-compose --version
# docker system prune -a --volumes

# ssitQLHcne5LvfWH3FR
# docker exec -it mongo mongosh -u Forgot -p 5LvfWH3FR1jOo1LPUfcACFooYJt --authenticationDatabase test
# git pull origin main
# {
#     'id': 106,
#     'inboundId': 1,
#     'enable': True,
#     'email': '12020a04-8606-4488-a7d4-b21e01bf094b',
#     'up': 0,
#     'down': 0,
#     'expiryTime': 1735174891876,
#     'total': 0,
#     'reset': 0
# }
# print(datetime.fromtimestamp(1734915691876/1000))
# upload=39718586350
# print(f"├─ ↑ Отправлено: {upload/1024/1024/1024:0.2f} ГБ")

# ngrok http --url=probably-stable-tortoise.ngrok-free.app 8080
# safd = {1, 2, 3, 4}
# print((f"{uuid4()}".encode()))
# print((timedelta(days=30)//10))

# ids = [
#     1770295162, 6316358679, 692184436, 1042070138, 547949137, 849822903, 8010428214, 1240108949, 7777327629,
#     765433968, 1426318435, 936598501, 1031926640, 1717921023, 1792883162, 159836975, 318877643, 687678911,
#     457574767, 1451476884, 775321734, 6244842561, 1729560465, 597392890, 1770295162, 753908039, 5084054845, 876969542,
#     572318370, 1162794031, 1489585156, 715881095, 700273209, 1220039756, 1060598177, 1084726555, 873965551,
#     883790514, 5364232955, 860358242, 5482852184, 1462075625, 1913585405, 7365530816, 6251257605, 7388408428,
#     6997721068, 2146215139, 6594097133, 523727612, 5912357295, 7470954241, 896148385, 1140019298, 675421286,
#     842053867, 7550187185, 6133064237, 922301826, 1682053112, 7248236042, 1063089542, 1938330856, 5363626020,
#     5231877043, 1142221479, 1074114959, 6522480240, 553078033, 633985222, 692175727, 1063089542, 753511174,
#     1868881309, 1012610779, 989474369
# ]


# with open('./data.txt', 'r') as f:
#     stroka = f.read()
#     stroka = stroka.replace("'", "")
#     print(stroka)
    # data = loads(stroka)

# print(data)
d = datetime.now()

print(datetime.fromtimestamp(d.timestamp()))