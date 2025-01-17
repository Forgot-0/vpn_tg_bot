

from typing import Any

from domain.entities.user import User


def convert_user_document_to_entity(document: dict[str, Any]) -> User:
    return User(
        id=document['_id'],
        server_id=document['server_id'],
        uuid=document['uuid'],
        is_premium=document['is_premium'],
        username=document['username'],
        fullname=document['fullname'],
        phone=document['phone'],
        referred_by=document.get('referred_by', None),
        referrals_count=document.get('referrals_count', 0),
    )


def convert_user_entity_to_document(user: User) -> dict[str, Any]:
    return {
        '_id': user.id,
        'server_id': user.server_id,
        'uuid': user.uuid,
        'is_premium': user.is_premium,
        'username': user.username,
        'fullname': user.fullname,
        'phone': user.phone,
        'referred_by': user.referred_by,
        'referrals_count': user.referrals_count,
    }