from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class InboundOption(BaseModel):
    id: int
    remark: str
    protocol: str
    port: int
    tlsFlowCapable: bool = False


class InboundOptionsResponse(BaseModel):
    success: bool
    obj: list[InboundOption] = Field(default_factory=list)


class ClientTraffic(BaseModel):
    up: int = 0
    down: int = 0
    enable: bool | None = None


class ClientListItem(BaseModel):
    email: str
    subId: str | None = None
    enable: bool = True
    totalGB: int = 0
    expiryTime: int = 0
    limitIp: int = 0
    reset: int = 0
    inboundIds: list[int] = Field(default_factory=list)
    traffic: ClientTraffic = Field(default_factory=ClientTraffic)
    createdAt: int | None = None
    updatedAt: int | None = None


class PagedClientSummary(BaseModel):
    total: int = 0
    active: int = 0
    online: list[str] = Field(default_factory=list)
    depleted: list[str] = Field(default_factory=list)
    expiring: list[str] = Field(default_factory=list)
    deactive: list[str] = Field(default_factory=list)


class PagedClientsPayload(BaseModel):
    items: list[ClientListItem] = Field(default_factory=list)
    total: int = 0
    filtered: int = 0
    page: int = 1
    pageSize: int = 25
    summary: PagedClientSummary = Field(default_factory=PagedClientSummary)


class PagedClientsResponse(BaseModel):
    success: bool
    obj: PagedClientsPayload


class ClientPayload(BaseModel):
    email: str
    subId: str | None = None
    id: str | None = None
    password: str | None = None
    auth: str | None = None
    flow: str | None = None
    totalGB: int = 0
    expiryTime: int = 0
    limitIp: int = 0
    tgId: int = 0
    comment: str = ""
    enable: bool = True
    reverse: dict[str, Any] | None = None


class AddClientRequest(BaseModel):
    client: ClientPayload
    inboundIds: list[int]


class ClientLinksResponse(BaseModel):
    success: bool
    obj: list[str] = Field(default_factory=list)


class TrafficPayload(BaseModel):
    email: str
    up: int = 0
    down: int = 0
    total: int = 0
    expiryTime: int = 0


class TrafficResponse(BaseModel):
    success: bool
    obj: TrafficPayload


class SubscriptionSettings(BaseModel):
    subEnable: bool = False
    subPort: int = 10882
    subPath: str = "/sub/"
    subDomain: str = ""
    subCertFile: str = ""


class ServerInboundSettings(BaseModel):
    id: int
    protocol: str
    streamSettings: dict[str, Any] = Field(default_factory=dict)


class ServerSettings(BaseModel):
    inbounds: dict[int, Literal["vless", "vmess", "trojan", "shadowsocks", "hysteria2"]]
    subscription: SubscriptionSettings = Field(default_factory=SubscriptionSettings)


