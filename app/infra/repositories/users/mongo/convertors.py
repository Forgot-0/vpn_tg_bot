

from typing import Any

from domain.entities.user import User


def convert_user_document_to_entity(document: dict[str, Any]) -> User:
    return User(
        id=document['_id'],
        tg_id=document['tg_id'],
        is_premium=document['is_premium'],
        tg_username=document['tg_username'],
    )


def convert_user_entity_to_document(user: User) -> dict[str, Any]:
    return {
        '_id': user.id,
        'tg_id': user.tg_id,
        'is_premium': user.is_premium,
        'tg_username': user.tg_username,
    }