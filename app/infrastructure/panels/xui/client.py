from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any
from urllib.parse import quote
from uuid import uuid4

from httpx import AsyncClient, Response

from app.application.interfaces.servers import PanelClient, PanelServerInfoResult
from app.domain.entities.access import ProvisionedAccess
from app.domain.entities.server import PanelConnection, VPNServer
from app.domain.entities.subscription import Subscription
from app.domain.values.servers import PanelType, ProtocolCode
from app.domain.values.subscriptions import AccessCredential, AccessFormat, ProvisioningStatus, RemoteAccessState

_BYTES_IN_GIB = Decimal(1024**3)
_SUPPORTED_LINK_PROTOCOLS = {
    ProtocolCode.VLESS,
    ProtocolCode.VMESS,
    ProtocolCode.TROJAN,
    ProtocolCode.SHADOWSOCKS,
    ProtocolCode.HYSTERIA2,
}


@dataclass
class ThreeXUIClient(PanelClient):
    client: AsyncClient

    @property
    def panel_type(self) -> PanelType:
        return PanelType.X3UI

    def _base_url(self, connection: PanelConnection) -> str:
        cfg = connection.endpoint
        scheme = "https" if cfg.use_ssl else "http"
        base_path = cfg.path.strip("/")
        if base_path:
            return f"{scheme}://{cfg.host}:{cfg.port}/{base_path}"
        return f"{scheme}://{cfg.host}:{cfg.port}"

    def _url(self, connection: PanelConnection, path: str) -> str:
        return f"{self._base_url(connection)}/{path.lstrip('/')}"

    async def login(self, connection: PanelConnection) -> None:
        if connection.credentials.api_token is not None:
            return

        if connection.credentials.username is not None:
            resp = await self.client.post(
                self._url(connection, "/login"),
                data={
                    "username": connection.credentials.username,
                    "password": connection.credentials.password,
                },
            )
            resp.raise_for_status()
            self._ensure_success(resp)

    async def create(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> ProvisionedAccess:
        await self.login(connection)

        email = self._client_email(server, subscription)
        inbound_ids = await self._resolve_inbound_ids(server, connection, subscription)
        payload = {
            "client": self._client_payload(server, subscription, email),
            "inboundIds": inbound_ids,
        }

        resp = await self._request(connection, "POST", "/panel/api/clients/add", json=payload)
        self._ensure_success(resp)

        credentials = await self._get_access_credentials(
            server,
            connection,
            email,
            self._subscription_id(server, subscription),
        )
        return ProvisionedAccess(
            id=uuid4(),
            subscription_id=subscription.id,
            server_id=server.id,
            panel_type=connection.panel_type,
            panel_client_id=email,
            inbound_ids=tuple(inbound_ids),
            credentials=credentials,
            status=ProvisioningStatus.ACTIVE,
            remote_state=RemoteAccessState.EXISTS,
        )

    async def delete(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> None:
        await self.login(connection)
        email = self._client_email(server, subscription)
        keep_traffic = "1" if server.panel_config.get("keep_traffic_on_delete") else "0"
        resp = await self._request(
            connection,
            "POST",
            f"/panel/api/clients/del/{quote(email, safe='')}",
            params={"keepTraffic": keep_traffic},
        )
        self._ensure_success(resp)

    async def sync_traffic(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> Decimal:
        await self.login(connection)
        email = self._client_email(server, subscription)
        resp = await self._request(
            connection,
            "GET",
            f"/panel/api/clients/traffic/{quote(email, safe='')}",
        )
        data = self._ensure_success(resp)
        traffic = data.get("obj") or {}
        used_bytes = int(traffic.get("up") or 0) + int(traffic.get("down") or 0)
        return Decimal(used_bytes) / _BYTES_IN_GIB

    async def get_info(
        self,
        *,
        server: VPNServer,
        connection: PanelConnection,
    ) -> PanelServerInfoResult:
        await self.login(connection)
        resp = await self._request(connection, "GET", "/panel/api/inbounds/options")
        data = self._ensure_success(resp)
        options = data.get("obj") or []
        protocols: set[ProtocolCode] = set()
        for option in options:
            if isinstance(option, dict):
                protocol = self._protocol_code(option.get("protocol"))
                if protocol:
                    protocols.add(protocol)
        return PanelServerInfoResult(
            supported_protocols=frozenset(protocols),
            panel_config=server.panel_config,
        )

    async def _get_access_credentials(
        self,
        server: VPNServer,
        connection: PanelConnection,
        email: str,
        sub_id: str,
    ) -> list[AccessCredential]:
        resp = await self._request(
            connection,
            "GET",
            f"/panel/api/clients/links/{quote(email, safe='')}",
        )
        data = self._ensure_success(resp)
        links = data.get("obj") or []
        credentials = [
            AccessCredential(
                format=AccessFormat.CONNECTION_STRING,
                value=link,
                protocol=self._protocol_from_link(link),
                panel_client_id=email,
                label=email,
            )
            for link in links
            if isinstance(link, str) and link
        ]

        subscription_url = self._subscription_url(server, connection, sub_id)
        if subscription_url is not None:
            credentials.append(
                AccessCredential(
                    format=AccessFormat.SUBSCRIPTION_URL,
                    value=subscription_url,
                    protocol=ProtocolCode.SUBSCRIPTION,
                    panel_client_id=email,
                    label=email,
                )
            )
        return credentials

    async def _request(
        self,
        connection: PanelConnection,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Response:
        headers = dict(kwargs.pop("headers", {}) or {})
        token = connection.credentials.api_token
        if token is not None:
            headers.setdefault("Authorization", f"Bearer {token}")
        return await self.client.request(
            method, self._url(connection, path), headers=headers, **kwargs
        )

    def _ensure_success(self, resp: Response) -> dict[str, Any]:
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise ValueError("3x-ui returned a non-object JSON response")
        if data.get("success") is not True:
            msg = data.get("msg") or data.get("message") or "3x-ui request failed"
            raise ValueError(str(msg))
        return data

    def _client_payload(
        self,
        server: VPNServer,
        subscription: Subscription,
        email: str,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "email": email,
            "subId": self._subscription_id(server, subscription),
            "totalGB": self._traffic_limit_bytes(subscription),
            "expiryTime": self._expiry_time_ms(subscription),
            "limitIp": subscription.spec.max_devices,
            "tgId": int(server.panel_config.get("tg_id", 0) or 0),
            "comment": self._client_comment(server, subscription),
            "enable": True,
        }
        for key in ("flow", "reverse", "reset"):
            if key in server.panel_config:
                payload[key] = server.panel_config[key]
        return payload

    async def _resolve_inbound_ids(
        self,
        server: VPNServer,
        connection: PanelConnection,
        subscription: Subscription,
    ) -> list[int]:
        requested_protocols = {
            p for p in subscription.spec.protocols if p != ProtocolCode.SUBSCRIPTION
        }
        configured_ids = self._configured_inbound_ids(server.panel_config, requested_protocols)
        if configured_ids:
            return configured_ids

        resp = await self._request(connection, "GET", "/panel/api/inbounds/options")
        data = self._ensure_success(resp)
        options = data.get("obj") or []
        inbound_ids: list[int] = []
        for option in options:
            if not isinstance(option, dict):
                continue
            protocol = self._protocol_code(option.get("protocol"))
            if requested_protocols and protocol not in requested_protocols:
                continue
            inbound_id = option.get("id")
            if isinstance(inbound_id, int):
                inbound_ids.append(inbound_id)

        inbound_ids = self._dedupe(inbound_ids)
        if not inbound_ids:
            raise ValueError("No matching 3x-ui inbounds found for subscription protocols")
        return inbound_ids

    def _subscription_url(
        self,
        server: VPNServer,
        connection: PanelConnection,
        sub_id: str,
    ) -> str | None:
        if not server.panel_config.get("include_subscription_url", False):
            return None

        quoted_sub_id = quote(sub_id, safe="")
        sub_domain = server.panel_config.get("sub_domain") or server.panel_config.get("subDomain")
        if sub_domain:
            base = str(sub_domain).rstrip("/")
        else:
            scheme = (
                "https"
                if server.panel_config.get("sub_use_ssl", connection.endpoint.use_ssl)
                else "http"
            )
            port = int(
                server.panel_config.get("sub_port", server.panel_config.get("subPort", 10882))
            )
            base = f"{scheme}://{connection.endpoint.host}:{port}"
        sub_path = str(
            server.panel_config.get("sub_path", server.panel_config.get("subPath", "/sub/"))
        )
        return f"{base}/{sub_path.strip('/')}/{quoted_sub_id}"

    # --- небольшие helpers (без изменений по логике) ---

    def _client_email(self, server: VPNServer, subscription: Subscription) -> str:
        for credential in subscription.access_credentials:
            if credential.panel_client_id:
                return credential.panel_client_id
        prefix = str(server.panel_config.get("client_email_prefix", "sub"))
        return f"{prefix}-{subscription.id.hex}"

    def _subscription_id(self, server: VPNServer, subscription: Subscription) -> str:
        prefix = str(server.panel_config.get("sub_id_prefix", ""))
        return f"{prefix}{subscription.id.hex}"

    def _client_comment(self, server: VPNServer, subscription: Subscription) -> str:
        template = server.panel_config.get("client_comment")
        if isinstance(template, str):
            return template.format(
                subscription_id=subscription.id, user_id=subscription.user_id
            )
        return f"subscription:{subscription.id}"

    def _traffic_limit_bytes(self, subscription: Subscription) -> int:
        if subscription.spec.traffic_limit_gb is None:
            return 0
        return int(subscription.spec.traffic_limit_gb * _BYTES_IN_GIB)

    def _expiry_time_ms(self, subscription: Subscription) -> int:
        if subscription.expires_at is not None:
            return self._date_end_ms(subscription.expires_at)
        if subscription.spec.duration_days is None:
            return 0
        expires_at = datetime.now(UTC) + timedelta(days=subscription.spec.duration_days)
        return int(expires_at.timestamp() * 1000)

    def _date_end_ms(self, value: date) -> int:
        dt = datetime.combine(value, time.max, tzinfo=UTC)
        return int(dt.timestamp() * 1000)

    def _configured_inbound_ids(
        self,
        panel_config: dict[str, Any],
        requested_protocols: set[ProtocolCode],
    ) -> list[int]:
        raw = (
            panel_config.get("inboundIds")
            or panel_config.get("inbound_ids")
            or panel_config.get("inbounds")
        )
        if raw is None:
            return []
        if isinstance(raw, list):
            return self._dedupe([int(item) for item in raw])
        if not isinstance(raw, dict):
            return []
        result: list[int] = []
        for key, value in raw.items():
            key_protocol = self._protocol_code(key)
            if key_protocol is not None:
                if not requested_protocols or key_protocol in requested_protocols:
                    result.extend(self._as_int_list(value))
                continue
            if str(key).isdigit():
                value_protocol = self._protocol_code(value)
                if not requested_protocols or value_protocol in requested_protocols:
                    result.append(int(key))
                continue
            if key == "default" and not result:
                result.extend(self._as_int_list(value))
        return self._dedupe(result)

    def _protocol_from_link(self, link: str) -> ProtocolCode | None:
        scheme = link.split(":", 1)[0].lower()
        if scheme == "hy2":
            scheme = ProtocolCode.HYSTERIA2.value
        protocol = self._protocol_code(scheme)
        if protocol in _SUPPORTED_LINK_PROTOCOLS:
            return protocol
        return None

    def _protocol_code(self, value: Any) -> ProtocolCode | None:
        if value is None:
            return None
        normalized = str(value).lower().replace("-", "")
        if normalized == "hysteria":
            normalized = ProtocolCode.HYSTERIA2.value
        for protocol in ProtocolCode:
            if protocol.value.replace("-", "") == normalized:
                return protocol
        return None

    def _as_int_list(self, value: Any) -> list[int]:
        if isinstance(value, (list, tuple)):
            return [int(item) for item in value]
        if value is None:
            return []
        return [int(value)]

    def _dedupe(self, values: list[int]) -> list[int]:
        result: list[int] = []
        seen: set[int] = set()
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
        return result
