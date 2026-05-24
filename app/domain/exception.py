from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    code: str
    status: int

    @property
    def message(self) -> str:
        return 'App error'

    @property
    def detail(self) -> dict | list:
        return {}


@dataclass(eq=False)
class UserNotFoundError(DomainError):
    code: str = "USER_NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return "User not found"


@dataclass(eq=False)
class UserAlreadyExistsError(DomainError):
    field: str = "email"
    code: str = "USER_ALREADY_EXISTS"
    status: int = 409

    @property
    def message(self) -> str:
        return f"User with this {self.field} already exists"

    @property
    def detail(self) -> dict:
        return {"field": self.field}


@dataclass(eq=False)
class InvalidCredentialsError(DomainError):
    code: str = "INVALID_CREDENTIALS"
    status: int = 401

    @property
    def message(self) -> str:
        return "Invalid credentials"


@dataclass(eq=False)
class RoleAssignmentError(DomainError):
    role: str = ""
    code: str = "ROLE_ASSIGNMENT_ERROR"
    status: int = 403

    @property
    def message(self) -> str:
        return f"Cannot assign role '{self.role}'"

    @property
    def detail(self) -> dict:
        return {"role": self.role}


@dataclass(eq=False)
class SubscriptionNotFoundError(DomainError):
    code: str = "SUBSCRIPTION_NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return "Subscription not found"


@dataclass(eq=False)
class SubscriptionPlanNotFoundError(DomainError):
    code: str = "SUBSCRIPTION_PLAN_NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return "Subscription plan not found"


@dataclass(eq=False)
class SubscriptionActivationError(DomainError):
    reason: str = ""
    code: str = "SUBSCRIPTION_ACTIVATION_ERROR"
    status: int = 422

    @property
    def message(self) -> str:
        return f"Cannot activate subscription: {self.reason}"

    @property
    def detail(self) -> dict:
        return {"reason": self.reason}


@dataclass(eq=False)
class NoEligibleServerError(DomainError):
    code: str = "NO_ELIGIBLE_SERVER"
    status: int = 503

    @property
    def message(self) -> str:
        return "No eligible VPN server found for the requested protocols"


@dataclass(eq=False)
class ProtocolNotAllowedError(DomainError):
    code: str = "PROTOCOL_NOT_ALLOWED"
    status: int = 422

    @property
    def message(self) -> str:
        return "One or more selected protocols are not allowed by this plan"


@dataclass(eq=False)
class SubscriptionAccessError(DomainError):
    code: str = "SUBSCRIPTION_ACCESS_DENIED"
    status: int = 403

    @property
    def message(self) -> str:
        return "Access to this subscription is denied"


@dataclass(eq=False)
class PaymentNotFoundError(DomainError):
    code: str = "PAYMENT_NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return "Payment order not found"


@dataclass(eq=False)
class PaymentAlreadyProcessedError(DomainError):
    code: str = "PAYMENT_ALREADY_PROCESSED"
    status: int = 409

    @property
    def message(self) -> str:
        return "Payment has already been processed"


@dataclass(eq=False)
class PaymentProviderError(DomainError):
    provider: str = ""
    code: str = "PAYMENT_PROVIDER_ERROR"
    status: int = 502

    @property
    def message(self) -> str:
        return f"Payment provider '{self.provider}' returned an error"

    @property
    def detail(self) -> dict:
        return {"provider": self.provider}
