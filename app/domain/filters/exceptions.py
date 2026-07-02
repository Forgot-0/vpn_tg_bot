from dataclasses import dataclass

from app.domain.errors import DomainError



@dataclass(eq=False, kw_only=True)
class PaginationParamsError(DomainError):
    field: str
    limit: int
    code: int = 400
    status: str = "PAGINATION_PARAMS"

    @property
    def message(self) -> str:
        return "Invalida pagination params"

    @property
    def detail(self) -> dict:
        return {
            self.field: self.limit
        }


@dataclass(eq=False, kw_only=True)
class ValueMustNotNoneError(DomainError):
    field: str
    code: int = 400
    status: str = "VALUE_MUST_NOT_NONE"

    @property
    def message(self) -> str:
        return "The value must not be empty"

    @property
    def detail(self) -> dict:
        return {
            "field": self.field
        }

@dataclass(eq=False, kw_only=True)
class AttributeNotExistError(DomainError):
    field: str
    code: int = 400
    status: str = "ATTRIBUTE_NOT_EXIST"

    @property
    def message(self) -> str:
        return "This attribute does not exist"

    @property
    def detail(self) -> dict:
        return {
            "attribute": self.field
        }
