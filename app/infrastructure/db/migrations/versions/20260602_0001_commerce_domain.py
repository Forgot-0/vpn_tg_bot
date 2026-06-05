"""create commerce and provisioning schema

Revision ID: 20260602_0001
Revises:
Create Date: 2026-06-02
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260602_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JSONB = postgresql.JSONB(astext_type=sa.Text())
UUID = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("email", sa.String(320), nullable=True, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True, unique=True),
        sa.Column("referral_code", sa.String(64), nullable=False, unique=True),
        sa.Column("referred_by", UUID, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("referrals_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "products",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("code", sa.String(64), nullable=False, unique=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("product_type", sa.String(32), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )

    op.create_table(
        "locations",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("country_code", sa.String(8), nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("city", sa.String(128), nullable=True),
        sa.Column("emoji", sa.String(16), nullable=False, server_default=""),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_locations_country_code", "locations", ["country_code"])

    op.create_table(
        "server_groups",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("location_id", UUID, sa.ForeignKey("locations.id", ondelete="SET NULL"), nullable=True),
        sa.Column("max_clients", sa.Integer(), nullable=True),
        sa.Column("max_traffic_gb", sa.Numeric(16, 4), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tags", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
    )
    op.create_index("ix_server_groups_location_id", "server_groups", ["location_id"])

    op.create_table(
        "panel_connections",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("panel_type", sa.String(32), nullable=False),
        sa.Column("endpoint", JSONB, nullable=False),
        sa.Column("credentials_encrypted", JSONB, nullable=False),
        sa.Column("config", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "vpn_servers",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("region_code", sa.String(16), nullable=False),
        sa.Column("panel_type", sa.String(32), nullable=False),
        sa.Column("panel_host", sa.String(255), nullable=False),
        sa.Column("panel_port", sa.Integer(), nullable=False),
        sa.Column("panel_path", sa.String(255), nullable=False, server_default="/"),
        sa.Column("panel_use_ssl", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("panel_username", sa.String(128), nullable=True),
        sa.Column("panel_password", sa.String(255), nullable=True),
        sa.Column("panel_two_factor_secret", sa.String(255), nullable=True),
        sa.Column("panel_config", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("supported_protocols", postgresql.ARRAY(sa.String(128)), nullable=False, server_default=sa.text("ARRAY[]::varchar[]")),
        sa.Column("supported_features", postgresql.ARRAY(sa.String(128)), nullable=False, server_default=sa.text("ARRAY[]::varchar[]")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("max_clients", sa.Integer(), nullable=True),
        sa.Column("current_clients", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("free", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("tags", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
    )
    op.create_index("ix_vpn_servers_region_code", "vpn_servers", ["region_code"])

    op.create_table(
        "plans",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("code", sa.String(64), nullable=False, unique=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("plan_type", sa.String(16), nullable=False),
        sa.Column("product_id", UUID, sa.ForeignKey("products.id", ondelete="SET NULL"), nullable=True),
        sa.Column("product_type", sa.String(32), nullable=False, server_default="vpn_subscription"),
        sa.Column("visibility", sa.String(16), nullable=False, server_default="public"),
        sa.Column("fixed_spec", JSONB, nullable=True),
        sa.Column("fixed_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("fixed_currency", sa.String(8), nullable=True),
        sa.Column("constraints", JSONB, nullable=True),
        sa.Column("pricing_rules", JSONB, nullable=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("allowed_region_codes", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("allowed_location_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("allowed_server_group_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_plans_product_id", "plans", ["product_id"])

    op.create_table(
        "prices",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("plan_id", UUID, sa.ForeignKey("plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False),
        sa.Column("price_type", sa.String(32), nullable=False),
        sa.Column("billing_interval", sa.String(16), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=True),
        sa.Column("traffic_limit_gb", sa.Numeric(16, 4), nullable=True),
        sa.Column("device_count", sa.Integer(), nullable=True),
        sa.Column("country_code", sa.String(2), nullable=True),
        sa.Column("tax_category", sa.String(64), nullable=True),
        sa.Column("promo_eligible", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("active_from", sa.Date(), nullable=True),
        sa.Column("active_to", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_prices_plan_id", "prices", ["plan_id"])

    op.create_table(
        "offers",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("plan_id", UUID, sa.ForeignKey("plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("price_id", UUID, sa.ForeignKey("prices.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("subtitle", sa.String(255), nullable=False, server_default=""),
        sa.Column("marketing_labels", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("terms", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("discount_percent", sa.Numeric(5, 2), nullable=True),
        sa.Column("trial_days", sa.Integer(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active_from", sa.Date(), nullable=True),
        sa.Column("active_to", sa.Date(), nullable=True),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_offers_plan_id", "offers", ["plan_id"])
    op.create_index("ix_offers_price_id", "offers", ["price_id"])
    op.create_index("ix_offers_status", "offers", ["status"])

    op.create_table(
        "orders",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("checkout_session_id", UUID, nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("line_items", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("total_currency", sa.String(8), nullable=True),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_index("ix_orders_checkout_session_id", "orders", ["checkout_session_id"])
    op.create_index("ix_orders_status", "orders", ["status"])

    op.create_table(
        "checkout_sessions",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_id", UUID, sa.ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("server_id", UUID, sa.ForeignKey("vpn_servers.id", ondelete="RESTRICT"), nullable=True),
        sa.Column("offer_id", UUID, sa.ForeignKey("offers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("price_id", UUID, sa.ForeignKey("prices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("order_id", UUID, sa.ForeignKey("orders.id", ondelete="SET NULL"), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("spec", JSONB, nullable=False),
        sa.Column("calculated_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("calculated_currency", sa.String(8), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_checkout_sessions_user_id", "checkout_sessions", ["user_id"])
    op.create_index("ix_checkout_sessions_plan_id", "checkout_sessions", ["plan_id"])
    op.create_index("ix_checkout_sessions_server_id", "checkout_sessions", ["server_id"])
    op.create_index("ix_checkout_sessions_order_id", "checkout_sessions", ["order_id"])
    op.create_index("ix_checkout_sessions_status", "checkout_sessions", ["status"])

    op.create_table(
        "payment_intents",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("checkout_session_id", UUID, sa.ForeignKey("checkout_sessions.id", ondelete="CASCADE"), nullable=True),
        sa.Column("order_id", UUID, sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=True),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("external_id", sa.String(128), nullable=True, unique=True),
        sa.Column("confirmation_url", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(128), nullable=True),
        sa.Column("provider_payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_payment_intents_checkout_session_id", "payment_intents", ["checkout_session_id"])
    op.create_index("ix_payment_intents_order_id", "payment_intents", ["order_id"])
    op.create_index("ix_payment_intents_user_id", "payment_intents", ["user_id"])
    op.create_index("ix_payment_intents_status", "payment_intents", ["status"])
    op.create_index("ix_payment_intents_idempotency_key", "payment_intents", ["idempotency_key"])

    op.create_table(
        "subscriptions",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_id", UUID, sa.ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("server_id", UUID, sa.ForeignKey("vpn_servers.id", ondelete="RESTRICT"), nullable=True),
        sa.Column("order_id", UUID, sa.ForeignKey("orders.id", ondelete="SET NULL"), nullable=True),
        sa.Column("spec", JSONB, nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("payment_intent_id", UUID, nullable=True),
        sa.Column("purchased_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("purchased_currency", sa.String(8), nullable=True),
        sa.Column("started_at", sa.Date(), nullable=True),
        sa.Column("expires_at", sa.Date(), nullable=True),
        sa.Column("current_period_start", sa.Date(), nullable=True),
        sa.Column("current_period_end", sa.Date(), nullable=True),
        sa.Column("used_traffic_gb", sa.Numeric(16, 4), nullable=False, server_default="0"),
        sa.Column("access_credentials", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("provisioned_access_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_subscriptions_user_id", "subscriptions", ["user_id"])
    op.create_index("ix_subscriptions_status", "subscriptions", ["status"])
    op.create_index("ix_subscriptions_payment_intent_id", "subscriptions", ["payment_intent_id"])
    op.create_index("ix_subscriptions_expires_at", "subscriptions", ["expires_at"])
    op.create_index("ix_subscriptions_order_id", "subscriptions", ["order_id"])
    op.create_index("ix_subscriptions_current_period_end", "subscriptions", ["current_period_end"])

    op.create_table(
        "inbounds",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("server_id", UUID, sa.ForeignKey("vpn_servers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("panel_inbound_id", sa.Integer(), nullable=False),
        sa.Column("protocol", sa.String(32), nullable=False),
        sa.Column("features", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("config", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_inbounds_server_id", "inbounds", ["server_id"])
    op.create_index("ix_inbounds_protocol", "inbounds", ["protocol"])

    op.create_table(
        "provisioned_accesses",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("subscription_id", UUID, sa.ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("server_id", UUID, sa.ForeignKey("vpn_servers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("panel_type", sa.String(32), nullable=False),
        sa.Column("panel_client_id", sa.String(255), nullable=False),
        sa.Column("inbound_ids", postgresql.ARRAY(sa.String(32)), nullable=False, server_default=sa.text("ARRAY[]::varchar[]")),
        sa.Column("credentials", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("remote_state", sa.String(32), nullable=False),
        sa.Column("used_traffic_gb", sa.Numeric(16, 4), nullable=False, server_default="0"),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_provisioned_accesses_subscription_id", "provisioned_accesses", ["subscription_id"])
    op.create_index("ix_provisioned_accesses_server_id", "provisioned_accesses", ["server_id"])
    op.create_index("ix_provisioned_accesses_panel_client_id", "provisioned_accesses", ["panel_client_id"])
    op.create_index("ix_provisioned_accesses_status", "provisioned_accesses", ["status"])


def downgrade() -> None:
    for table_name in (
        "provisioned_accesses",
        "inbounds",
        "subscriptions",
        "payment_intents",
        "checkout_sessions",
        "orders",
        "offers",
        "prices",
        "plans",
        "vpn_servers",
        "panel_connections",
        "server_groups",
        "locations",
        "products",
        "users",
    ):
        op.drop_table(table_name)
