from enum import StrEnum
from uuid import UUID

from app.domain.values.base import BaseValueObject
from app.domain.exception.base import NotEmptyException


class UserId(BaseValueObject[UUID]):
    def validate(self):
        if not self.value:
            raise NotEmptyException(field_name="user_id")

    def as_generic_type(self) -> str:
        return str(self.value)



class UserRole(StrEnum):
    OWNER = "owner"
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

    @property
    def is_assignable(self) -> bool:
        return self != UserRole.SUPER_ADMIN

    @property
    def is_changeable(self) -> bool:
        return self != UserRole.SUPER_ADMIN