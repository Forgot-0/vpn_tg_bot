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

    @property
    def detail(self) -> dict:
        return {"field_name": self.field_name}


@dataclass(kw_only=True)
class CanNotReferalYourselfException(DomainException):
    referral_id: str
    code: str = "REFERRAL_CONFLICT"
    status: int = 400

    @property
    def message(self) -> str:
        return "User cannot refer themself"

    @property
    def detail(self) -> dict:
        return {
            "referral_id": self.referral_id
        }


@dataclass(kw_only=True)
class SubscriptionPendingException(DomainException):
    subscription_id: str
    code: str = "SUBSCRIPTION_CONFLICT"
    status: int = 400

    @property
    def message(self) -> str:
        return "Cannot renew a pending subscription"

    @property
    def detail(self) -> dict:
        return {
            "subscription_id": self.subscription_id
        }


@dataclass(kw_only=True)
class NotFoundProtocolException(DomainException):
    protocol_type: str
    code: str = "NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return ""

    @property
    def detail(self) -> dict:
        return {
            "protocol": self.protocol_type
        }

@dataclass(kw_only=True)
class AlreadyExistProtocolException(DomainException):
    protocol_type: str
    code: str = "ALREADY_EXIST"
    status: int = 400

    @property
    def message(self) -> str:
        return ""

    @property
    def detail(self) -> dict:
        return {
            "protocol": self.protocol_type
        }

