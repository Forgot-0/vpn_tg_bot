import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.base import BaseModelORM



class UserModel(BaseModelORM):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")

    email: Mapped[str | None] = mapped_column(String(320), unique=True, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    telegram_id: Mapped[int | None] = mapped_column(
        Integer, unique=True, nullable=True, index=True
    )

    referral_code: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    referred_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    referrals_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    referrer: Mapped["UserModel | None"] = relationship(
        "UserModel", remote_side="UserModel.id", foreign_keys=[referred_by]
    )

    __table_args__ = (
        Index("ix_users_email_lower", email, unique=True),
    )
