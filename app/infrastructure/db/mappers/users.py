from typing import overload

from app.domain.entities.user import User
from app.domain.values.users import UserRole
from app.infrastructure.db.models.user import UserModel


class UserMapper:
    @staticmethod
    def from_user_domain_to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            role=user.role.value,
            email=user.email,
            password_hash=user.password_hash,
            telegram_id=user.telegram_id,
            referral_code=user.referral_code,
            referred_by=user.referred_by,
            referrals_count=user.referrals_count,
            is_active=user.is_active,
            created_at=user.created_at,
        )

    @overload
    @staticmethod
    def from_user_model_to_domain(user_model: None) -> None:
        ...

    @overload
    @staticmethod
    def from_user_model_to_domain(user_model: UserModel) -> User:
        ...

    @staticmethod
    def from_user_model_to_domain(user_model: UserModel | None) -> User | None:
        if user_model is None:
            return None

        return User(
            id=user_model.id,
            role=UserRole(user_model.role),
            email=user_model.email,
            password_hash=user_model.password_hash,
            telegram_id=user_model.telegram_id,
            referral_code=user_model.referral_code,
            referred_by=user_model.referred_by,
            referrals_count=user_model.referrals_count,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
        )
