

from typing import Any

from app.domain.entities.user import User
from app.domain.values.users import UserId, UserRole
from app.infrastructure.db.convertors.subscription import (
    convert_subscription_document_to_entity,
    convert_subscription_entity_to_document
)


def convert_user_entity_to_document(user: User) -> dict[str, Any]:
    return {
            '_id': user.id.value,
            'role': user.role.value,
            'telegram_id': user.telegram_id,
            'is_premium': user.is_premium,
            'username': user.username,
            'fullname': user.fullname,
            'phone': user.phone,
            'referred_by': user.referred_by.value if user.referred_by else None,
            'referrals_count': user.referrals_count,
            'created_at': user.created_at,
            'subscriptions': [convert_subscription_entity_to_document(s) for s in user.subscriptions]
        }

def convert_user_document_to_entity(data: dict[str, Any]) -> User:
    return User(
            id=UserId(data["_id"]),
            role=UserRole(data['role']),
            telegram_id=data['telegram_id'],
            is_premium=data['is_premium'],
            username=data['username'],
            fullname=data['fullname'],
            phone=data['phone'],
            referred_by=UserId(data['referred_by']) if data['referred_by'] else None,
            referrals_count=data['referrals_count'],
            created_at=data['created_at'],
            subscriptions=[convert_subscription_document_to_entity(s) for s in data.get("subscriptions", [])]
        )
