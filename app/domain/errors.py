from dataclasses import dataclass, field


@dataclass(eq=False)
class DomainError(Exception):
    code: str = "DOMAIN_ERROR"
    status: int = 400

    @property
    def message(self) -> str:
        return "Domain error"

    @property
    def detail(self) -> dict:
        return {}


@dataclass(eq=False)
class NotFoundError(DomainError):
    code: str = "NOT_FOUND"
    status: int = 404

    entity: str = ""
    entity_id: str = ""

    @property
    def message(self) -> str:
        return f"{self.entity} not found" if self.entity else "Not found"

    @property
    def detail(self) -> dict:
        return {"entity": self.entity, "id": self.entity_id}


@dataclass(eq=False)
class AlreadyExistsError(DomainError):
    code: str = "ALREADY_EXISTS"
    status: int = 409

    reason: str = ""

    @property
    def message(self) -> str:
        return self.reason or "Already exists"


@dataclass(eq=False)
class InvalidStateTransitionError(DomainError):
    code: str = "INVALID_STATE_TRANSITION"
    status: int = 422

    reason: str = ""

    @property
    def message(self) -> str:
        return f"Invalid state transition: {self.reason}"

    @property
    def detail(self) -> dict:
        return {"reason": self.reason}


@dataclass(eq=False)
class BusinessRuleViolationError(DomainError):
    code: str = "BUSINESS_RULE_VIOLATION"
    status: int = 422

    reason: str = ""

    @property
    def message(self) -> str:
        return self.reason or "Business rule violated"

    @property
    def detail(self) -> dict:
        return {"reason": self.reason}


@dataclass(eq=False)
class SpecValidationError(DomainError):
    code: str = "SPEC_VALIDATION_ERROR"
    status: int = 422

    violations: list[str] = field(default_factory=list)

    @property
    def message(self) -> str:
        return f"Subscription spec is invalid: {'; '.join(self.violations)}"

    @property
    def detail(self) -> dict:
        return {"violations": self.violations}
