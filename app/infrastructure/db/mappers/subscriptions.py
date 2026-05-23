from decimal import Decimal

from app.domain.entities.subscription import (
    AccessRotation,
    Subscription,
    SubscriptionPlan,
    SubscriptionRenewal,
)
from app.domain.values.subscriptions import (
    AccessArtifact,
    AccessFormat,
    BillingMode,
    DeviceCount,
    DurationDays,
    Money,
    PlanFeature,
    PlanFeatureCode,
    SubscriptionStatus,
    TrafficQuota,
    VPNProtocol,
)
from app.infrastructure.db.models.subscriptions import (
    SubscriptionModel,
    SubscriptionPlanModel,
)


class SubscriptionPlanMapper:
    @staticmethod
    def to_domain(model: SubscriptionPlanModel) -> SubscriptionPlan:
        return SubscriptionPlan(
            id=model.id,
            code=model.code,
            name=model.name,
            billing_mode=BillingMode(model.billing_mode),
            duration=DurationDays(model.duration_days) if model.duration_days else None,
            traffic_quota=TrafficQuota(model.traffic_quota_gb) if model.traffic_quota_gb else None,
            max_devices=DeviceCount(model.max_devices) if model.max_devices else None,
            allowed_protocols=frozenset(VPNProtocol(p) for p in model.allowed_protocols),
            included_features=frozenset(
                PlanFeature(
                    code=PlanFeatureCode(f["code"]),
                    quantity=Decimal(f.get("quantity", "1")),
                )
                for f in model.included_features
            ),
            fixed_price=Money(
                amount=model.fixed_price_amount,
                currency=model.fixed_price_currency,
            ) if model.fixed_price_amount is not None else None,
        )

    @staticmethod
    def to_model(entity: SubscriptionPlan) -> SubscriptionPlanModel:
        return SubscriptionPlanModel(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            billing_mode=entity.billing_mode.value,
            duration_days=entity.duration.value if entity.duration else None,
            traffic_quota_gb=entity.traffic_quota.value if entity.traffic_quota else None,
            max_devices=entity.max_devices.value if entity.max_devices else None,
            allowed_protocols=[p.value for p in entity.allowed_protocols],
            included_features=[
                {"code": f.code.value, "quantity": str(f.quantity)}
                for f in entity.included_features
            ],
            fixed_price_amount=entity.fixed_price.amount if entity.fixed_price else None,
            fixed_price_currency=entity.fixed_price.currency if entity.fixed_price else "USD",
        )

    @staticmethod
    def update_model(model: SubscriptionPlanModel, entity: SubscriptionPlan) -> None:
        model.name = entity.name
        model.billing_mode = entity.billing_mode.value
        model.duration_days = entity.duration.value if entity.duration else None
        model.traffic_quota_gb = entity.traffic_quota.value if entity.traffic_quota else None
        model.max_devices = entity.max_devices.value if entity.max_devices else None
        model.allowed_protocols = [p.value for p in entity.allowed_protocols]
        model.included_features = [
            {"code": f.code.value, "quantity": str(f.quantity)}
            for f in entity.included_features
        ]
        model.fixed_price_amount = entity.fixed_price.amount if entity.fixed_price else None
        model.fixed_price_currency = entity.fixed_price.currency if entity.fixed_price else "USD"


class SubscriptionMapper:
    @staticmethod
    def to_domain(model: SubscriptionModel) -> Subscription:
        return Subscription(
            id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            server_id=model.server_id,
            protocols=frozenset(VPNProtocol(p) for p in model.protocols),
            devices=DeviceCount(model.devices),
            status=SubscriptionStatus(model.status),
            started_at=model.started_at,
            expires_at=model.expires_at,
            purchased_price=Money(
                amount=model.purchased_price_amount,
                currency=model.purchased_price_currency,
            ) if model.purchased_price_amount is not None else None,
            used_traffic_gb=model.used_traffic_gb or Decimal("0"),
            access_items=[
                AccessArtifact(
                    format=AccessFormat(a["format"]),
                    value=a["value"],
                    external_id=a.get("external_id"),
                )
                for a in model.access_items
            ],
            renewals=[
                SubscriptionRenewal(
                    id=r.id,
                    subscription_id=r.subscription_id,
                    renewed_at=r.renewed_at,
                    previous_expires_at=r.previous_expires_at,
                    new_expires_at=r.new_expires_at,
                    renewal_period_days=r.renewal_period_days,
                    price_paid=Money(r.price_paid_amount, r.price_paid_currency),
                    payment_id=r.payment_id,
                    renewed_by=r.renewed_by,
                )
                for r in model.renewals
            ],
            access_rotations=[
                AccessRotation(
                    id=rot.id,
                    subscription_id=rot.subscription_id,
                    rotated_at=rot.rotated_at,
                    reason=rot.reason,
                    old_access_items=[
                        AccessArtifact(
                            format=AccessFormat(a["format"]),
                            value=a["value"],
                            external_id=a.get("external_id"),
                        )
                        for a in rot.old_access_items
                    ],
                    new_access_items=[
                        AccessArtifact(
                            format=AccessFormat(a["format"]),
                            value=a["value"],
                            external_id=a.get("external_id"),
                        )
                        for a in rot.new_access_items
                    ],
                    rotated_by=rot.rotated_by,
                )
                for rot in model.access_rotations
            ],
        )

    @staticmethod
    def to_model(entity: Subscription) -> SubscriptionModel:
        return SubscriptionModel(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            server_id=entity.server_id,
            protocols=[p.value for p in entity.protocols],
            devices=entity.devices.value,
            status=entity.status.value,
            started_at=entity.started_at,
            expires_at=entity.expires_at,
            purchased_price_amount=entity.purchased_price.amount if entity.purchased_price else None,
            purchased_price_currency=entity.purchased_price.currency if entity.purchased_price else "USD",
            used_traffic_gb=entity.used_traffic_gb,
            access_items=[
                {
                    "format": a.format.value,
                    "value": a.value,
                    "external_id": a.external_id,
                }
                for a in entity.access_items
            ],
        )

    @staticmethod
    def update_model(model: SubscriptionModel, entity: Subscription) -> None:
        model.status = entity.status.value
        model.started_at = entity.started_at
        model.expires_at = entity.expires_at
        model.purchased_price_amount = entity.purchased_price.amount if entity.purchased_price else None
        model.purchased_price_currency = entity.purchased_price.currency if entity.purchased_price else "USD"
        model.used_traffic_gb = entity.used_traffic_gb
        model.access_items = [
            {
                "format": a.format.value,
                "value": a.value,
                "external_id": a.external_id,
            }
            for a in entity.access_items
        ]
        model.protocols = [p.value for p in entity.protocols]
        model.devices = entity.devices.value
