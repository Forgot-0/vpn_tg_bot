from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

import httpx

from app.application.dtos.payments import GatewayPaymentResult, GatewayStatusResult
from app.application.interfaces.payments import PaymentGateway
from app.configs.app import app_config
from app.domain.entities.payment import PaymentOrder
from app.domain.values.payments import PaymentProvider, PaymentStatus


_YOOKASSA_STATUS_MAP: dict[str, PaymentStatus] = {
    "pending": PaymentStatus.PENDING,
    "waiting_for_capture": PaymentStatus.WAITING_FOR_CAPTURE,
    "succeeded": PaymentStatus.SUCCEEDED,
    "canceled": PaymentStatus.CANCELLED,
}


@dataclass
class YooKassaPaymentGateway(PaymentGateway):
    api_base: str = "https://api.yookassa.ru/v3"
    timeout: float = 30.0

    @property
    def provider(self) -> PaymentProvider:
        return PaymentProvider.YOOKASSA

    def _auth_header(self) -> str:
        token = base64.b64encode(
            f"{app_config.PAYMENT_ID}:{app_config.PAYMENT_SECRET}".encode()
        ).decode()
        return f"Basic {token}"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": self._auth_header(),
            "Content-Type": "application/json",
            "Idempotence-Key": str(uuid4()),
        }

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict | None = None,
    ) -> dict:
        url = f"{self.api_base}{path}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method,
                url,
                headers=self._headers(),
                json=json_body,
            )

        if response.status_code >= 400:
            raise RuntimeError(
                f"YooKassa request failed ({response.status_code}): {response.text}"
            )

        payload = response.json()
        if not isinstance(payload, dict):
            raise RuntimeError("YooKassa returned unexpected payload")
        return payload

    @staticmethod
    def _map_status(raw_status: str) -> PaymentStatus:
        return _YOOKASSA_STATUS_MAP.get(raw_status, PaymentStatus.FAILED)

    @staticmethod
    def _format_amount(amount: Decimal) -> str:
        return f"{amount.quantize(Decimal('0.01')):.2f}"

    async def create_payment(
        self,
        order: PaymentOrder,
        *,
        return_url: str,
    ) -> GatewayPaymentResult:
        body = {
            "amount": {
                "value": self._format_amount(order.amount.amount),
                "currency": order.amount.currency,
            },
            "capture": True,
            "confirmation": {
                "type": "redirect",
                "return_url": return_url,
            },
            "description": f"Subscription payment {order.subscription_id}",
            "metadata": {
                "payment_order_id": str(order.id),
                "subscription_id": str(order.subscription_id),
                "user_id": str(order.user_id),
            },
        }
        payload = await self._request("POST", "/payments", json_body=body)
        status = self._map_status(payload["status"])
        confirmation = payload.get("confirmation") or {}
        return GatewayPaymentResult(
            external_id=payload["id"],
            status=status,
            confirmation_url=confirmation.get("confirmation_url"),
        )

    async def get_status(self, external_id: str) -> GatewayStatusResult:
        payload = await self._request("GET", f"/payments/{external_id}")
        status = self._map_status(payload["status"])
        paid_at = None
        if status == PaymentStatus.SUCCEEDED:
            captured_at = payload.get("captured_at") or payload.get("paid_at")
            if captured_at:
                paid_at = datetime.fromisoformat(captured_at.replace("Z", "+00:00"))
            else:
                paid_at = datetime.now(UTC)
        return GatewayStatusResult(
            external_id=payload["id"],
            status=status,
            paid_at=paid_at,
        )

    async def cancel_payment(self, external_id: str) -> None:
        await self._request("POST", f"/payments/{external_id}/cancel")

    async def refund_payment(
        self,
        external_id: str,
        *,
        amount_to_refund: float | None = None,
    ) -> None:
        payment = await self._request("GET", f"/payments/{external_id}")
        body: dict = {"payment_id": external_id}
        if amount_to_refund is not None:
            currency = payment["amount"]["currency"]
            body["amount"] = {
                "value": self._format_amount(Decimal(str(amount_to_refund))),
                "currency": currency,
            }
        await self._request("POST", "/refunds", json_body=body)
