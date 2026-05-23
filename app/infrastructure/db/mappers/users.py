from app.domain.entities.user import User
from app.domain.values.users import UserId, UserRole
from app.infrastructure.db.models.users import UserModel


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            role=UserRole(model.role),
            email=model.email,
            password_hash=model.password_hash,
            telegram_id=model.telegram_id,
            referral_code=model.referral_code,
            referred_by=UserId(model.referred_by) if model.referred_by else None,
            referrals_count=model.referrals_count,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            role=entity.role.value,
            email=entity.email,
            password_hash=entity.password_hash,
            telegram_id=entity.telegram_id,
            referral_code=entity.referral_code,
            referred_by=entity.referred_by.value if entity.referred_by else None,
            referrals_count=entity.referrals_count,
            created_at=entity.created_at,
        )
