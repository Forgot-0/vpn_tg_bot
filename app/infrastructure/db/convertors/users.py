

from typing import Any

from domain.entities.user import User


def convert_user_document_to_entity(document: dict[str, Any]) -> User:
    return User(
        id=document['_id'],
        is_premium=document['is_premium'],
        username=document['username'],
        fullname=document['fullname'],
        phone=document['phone']
    )


def convert_user_entity_to_document(user: User) -> dict[str, Any]:
    return {
        '_id': user.id,
        'is_premium': user.is_premium,
        'username': user.username,
        'fullname': user.fullname,
        'phone': user.phone,
    }