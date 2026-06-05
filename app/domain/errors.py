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


@dataclass(eq=False)
class PaymentNotFoundError(NotFoundError):
    code: str = "PAYMENT_NOT_FOUND"
    entity: str = "PaymentIntent"


@dataclass(eq=False)
class PaymentAlreadyTerminalError(DomainError):
    code: str = "PAYMENT_ALREADY_TERMINAL"
    status: int = 409

    @property
    def message(self) -> str:
        return "Payment is already in a terminal state"


@dataclass(eq=False)
class PaymentFailedError(DomainError):
    code: str = "PAYMENT_FAILED"
    status: int = 402

    @property
    def message(self) -> str:
        return "Payment failed"


@dataclass(eq=False)
class CheckoutNotFoundError(NotFoundError):
    code: str = "CHECKOUT_NOT_FOUND"
    entity: str = "CheckoutSession"


@dataclass(eq=False)
class SubscriptionNotFoundError(NotFoundError):
    code: str = "SUBSCRIPTION_NOT_FOUND"
    entity: str = "Subscription"


@dataclass(eq=False)
class ServerNotFoundError(NotFoundError):
    code: str = "SERVER_NOT_FOUND"
    entity: str = "VPNServer"


@dataclass(eq=False)
class NoAvailableServerError(DomainError):
    code: str = "NO_AVAILABLE_SERVER"
    status: int = 503

    @property
    def message(self) -> str:
        return "No available server for the requested configuration"


@dataclass(eq=False)
class PanelConnectionNotFoundError(NotFoundError):
    code: str = "PANEL_CONNECTION_NOT_FOUND"
    entity: str = "PanelConnection"


@dataclass(eq=False)
class PanelConnectionInactiveError(DomainError):
    code: str = "PANEL_CONNECTION_INACTIVE"
    status: int = 503

    @property
    def message(self) -> str:
        return "Panel connection is not active"


@dataclass(eq=False)
class PlanNotFoundError(NotFoundError):
    code: str = "PLAN_NOT_FOUND"
    entity: str = "Plan"


@dataclass(eq=False)
class PlanNotActiveError(DomainError):
    code: str = "PLAN_NOT_ACTIVE"
    status: int = 422

    @property
    def message(self) -> str:
        return "Plan is not active"


@dataclass(eq=False)
class UserNotFoundError(NotFoundError):
    code: str = "USER_NOT_FOUND"
    entity: str = "User"


@dataclass(eq=False)
class UserAlreadyExistsError(DomainError):
    code: str = "USER_ALREADY_EXISTS"
    status: int = 409

    @property
    def message(self) -> str:
        return "User with this email already exists"


@dataclass(eq=False)
class InvalidCredentialsError(DomainError):
    code: str = "INVALID_CREDENTIALS"
    status: int = 401

    @property
    def message(self) -> str:
        return "Invalid username or password"


@dataclass(eq=False)
class PasswordMismatchError(DomainError):
    code: str = "PASSWORD_MISMATCH"
    status: int = 422

    @property
    def message(self) -> str:
        return "Passwords do not match"


@dataclass(eq=False)
class InvalidTokenError(DomainError):
    code: str = "INVALID_TOKEN"
    status: int = 401

    @property
    def message(self) -> str:
        return "Token is invalid or expired"


@dataclass(eq=False)
class SubscriptionNotReadyForProvisioningError(DomainError):
    code: str = "SUBSCRIPTION_NOT_READY_FOR_PROVISIONING"
    status: int = 422

    status_value: str = ""

    @property
    def message(self) -> str:
        if self.status_value:
            return f"Subscription is not ready for provisioning (status: {self.status_value})"
        return "Subscription is not ready for provisioning"

    @property
    def detail(self) -> dict:
        return {"status": self.status_value} if self.status_value else {}


@dataclass(eq=False)
class SubscriptionMissingServerError(DomainError):
    code: str = "SUBSCRIPTION_MISSING_SERVER"
    status: int = 422

    @property
    def message(self) -> str:
        return "Subscription has no associated server"


@dataclass(eq=False)
class InvalidJwtTokenError(DomainError):
    code: str = "INVALID_JWT_TOKEN"
    status: int = 401

    @property
    def message(self) -> str:
        return "JWT token is invalid"


@dataclass(eq=False)
class ExpiredJwtTokenError(DomainError):
    code: str = "EXPIRED_JWT_TOKEN"
    status: int = 401

    @property
    def message(self) -> str:
        return "JWT token has expired"


@dataclass(eq=False)
class SubscriptionNotRenewableError(DomainError):
    code: str = "SUBSCRIPTION_NOT_RENEWABLE"
    status: int = 422

    status_value: str = ""
    reason: str = ""

    @property
    def message(self) -> str:
        if self.reason:
            return self.reason
        if self.status_value:
            return f"Subscription cannot be renewed (status: {self.status_value})"
        return "Subscription cannot be renewed"

    @property
    def detail(self) -> dict:
        detail: dict[str, str] = {}
        if self.status_value:
            detail["status"] = self.status_value
        if self.reason:
            detail["reason"] = self.reason
        return detail


@dataclass(eq=False)
class ProvisioningFailedError(DomainError):
    code: str = "PROVISIONING_FAILED"
    status: int = 502

    reason: str = ""

    @property
    def message(self) -> str:
        return f"Failed to provision subscription: {self.reason}"

    @property
    def detail(self) -> dict:
        return {"reason": self.reason}


@dataclass(eq=False)
class PanelClientNotRegisteredError(DomainError):
    code: str = "PANEL_CLIENT_NOT_REGISTERED"
    status: int = 500

    @property
    def message(self) -> str:
        return "Panel client is not registered"
