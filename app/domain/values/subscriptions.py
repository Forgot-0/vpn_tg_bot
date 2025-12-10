from uuid import UUID

from app.domain.exception.base import NotEmptyException
from app.domain.values.base import BaseValueObject


class SubscriptionId(BaseValueObject[UUID]):
    def validate(self):
        if not self.value:
            raise NotEmptyException(field_name="SubscriptionId")

    def as_generic_type(self) -> str:
        return str(self.value)

