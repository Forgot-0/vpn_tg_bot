from dataclasses import dataclass, field


@dataclass(eq=False)
class DomainException(Exception):
    code: str
    status: int

    @property
    def message(self) -> str:
        return 'App error'

    @property
    def detail(self) -> dict | list:
        return {}


@dataclass(kw_only=True)
class NotEmptyException(DomainException):
    field_name: str
    code: str = "VALIDATION_ERROR"
    status: int = 400


    @property
    def message(self) -> str:
        return "The field cannot be empty"


@dataclass(kw_only=True)
class EntityNotFoundException(DomainException):
    entity: str | None = None
    code: str = "ENTITY_NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return f'{self.entity or "Entity"} not found'


@dataclass(kw_only=True)
class EntityConflictException(DomainException):
    entity: str | None = None
    code: str = "ENTITY_CONFLICT"
    status: int = 409

    @property
    def message(self) -> str:
        return f'{self.entity or "Entity"} conflict'


@dataclass(kw_only=True)
class InvalidEntityStateException(DomainException):
    detail: str | None = None
    code: str = "INVALID_ENTITY_STATE"
    status: int = 400

    @property
    def message(self) -> str:
        return self.detail or 'Invalid entity state'

