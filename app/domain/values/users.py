from uuid import UUID

from domain.values.base import BaseValueObject


class UserId(BaseValueObject[UUID]):
    def validate(self):
        if not self.value:
            raise 

    def as_generic_type(self) -> str:
        return str(self.value)
