# from dataclasses import dataclass, field
# from datetime import datetime, timedelta
# from uuid import UUID, uuid4
# from enum import Enum


# class ProtocolType(Enum):
#     vless = "VLESS"
#     mock = "MOCK"


# class ApiType(Enum):
#     x_ui = "3X-UI"
#     mock = "MOCK"

# @dataclass
# class VPNConfig:
#     protocol_type: ProtocolType
#     config: str

# @dataclass(frozen=True)
# class Region:
#     flag: str
#     name: str
#     code: str

# @dataclass
# class Subscription():
#     id: UUID = field(default_factory=lambda: uuid4(), kw_only=True)
#     duration: int
#     start_date: datetime = field(default_factory=datetime.now, kw_only=True)

#     device_count: int

#     server_id: UUID
#     region: Region
    
#     user_id: UUID

#     protocol_types: list[ProtocolType]

#     @property
#     def end_date(self) -> datetime:
#         return self.start_date + timedelta(days=self.duration)

#     def is_active(self) -> bool:
#         return datetime.now() < self.start_date + timedelta(days=self.duration)

#     def upgrade_devices(self, new_device_count: int):
#         self.device_count = new_device_count

#     def change_region(self, new_region: Region):
#         self.region = new_region


# @dataclass
# class SubscriptionPricingService:

#     daily_rate: float
#     device_rate_multiplier: float
#     region_multipliers: dict[Region, float]
#     protocol_multipliers: dict[ProtocolType, float]

#     def calculate(self, subscription: Subscription) -> float:
#         base_cost = self.daily_rate * subscription.duration

#         devices_cost = base_cost * subscription.device_count * self.device_rate_multiplier

#         region_coef = self.region_multipliers.get(subscription.region, 1.0)
#         region_cost = base_cost * (region_coef - 1)

#         protocols_cost = sum(
#             base_cost * self.protocol_multipliers.get(protocol, 0)
#             for protocol in subscription.protocol_types
#         )

#         total = base_cost + devices_cost + region_cost + protocols_cost
#         return round(total, 2)


# s = SubscriptionPricingService(
#             daily_rate=2,
#             device_rate_multiplier=0.5,
#             region_multipliers={
#                 Region("🇳🇱", "Нидерланды", "NL"): 1.0,
#             },
#             protocol_multipliers={
#                 ProtocolType.vless: 0.15
#             }
#         )

# s = s.calculate(Subscription(360, 10, uuid4(), Region("🇳🇱", "Нидерланды", "NL"), uuid4(), [ProtocolType("VLESS")]))
# print(s, 99*12)

# s = {Region("🇳🇱", "Нидерланды", "NL"), Region("🇳🇱", "Нидерланды", "NL")}
# print(s)
# ngrok http --url=probably-stable-tortoise.ngrok-free.app 8080



from datetime import datetime, timedelta


print((datetime.now() - (datetime.now()-timedelta(days=90) + timedelta(days=30))))

t = {
    "container_created_at": "2025-05-25T16:39:58.138412034Z",
    "container_id":"0bb9e42aa1c2992275a61f2ca7df6d000ed2f74ac77504e08888a78b285d6662",
    "container_name":"app",
    "host":"e9fd98aa2fec",
    "image":"docker_compose-app",
    "label":{
        "com.docker.compose.config-hash":"362858e5b202e8e7b14024b9b1dc5c49765e3cc9c34bd14860e9518a20541024",
        "com.docker.compose.container-number":"1",
        "com.docker.compose.depends_on":"",
        "com.docker.compose.image":"sha256:4f2efdfb1e4a538fa0a4b04b6702a9a8697589a6910d28a90deb7ba9a13764bc",
        "com.docker.compose.oneoff":"False",
        "com.docker.compose.project":"docker_compose",
        "com.docker.compose.project.config_files":"/home/forgot/vpn_tg_bot/docker_compose/app.yaml",
        "com.docker.compose.project.environment_file":"/home/forgot/vpn_tg_bot/.env",
        "com.docker.compose.project.working_dir":"/home/forgot/vpn_tg_bot/docker_compose",
        "com.docker.compose.service":"app","com.docker.compose.version":"2.32.4"
    },
    "message":{
        "event":"Update id=128778615 is not handled. Duration 0 ms by bot id=5208514073",
        "func_name":"feed_update",
        "level":"info",
        "lineno":172,
        "logger":"aiogram.event",
        "timestamp":"2025-05-25 16:41:15.140323"
    },
    "source_type":"docker_logs",
    "stream":"stderr"
}
