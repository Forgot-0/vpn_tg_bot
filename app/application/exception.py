from dataclasses import dataclass

from app.domain.exception.base import DomainException




@dataclass(eq=False)
class ApplicationException(DomainException):
    code: str = "APPLICATION_EXCEPTION"
    status: int = 400

    @property
    def messege(self):
        return 'Application exception'


@dataclass(kw_only=True)
class NotFoundActiveSubscriptionException(ApplicationException):
    user_id: str
    code: str = "NOT_FOUND"
    status: int = 404

    @property
    def message(self):
        return f'The user has no active subscriptions'

    @property
    def detail(self):
        return {"user_id": self.user_id}


@dataclass(kw_only=True)
class BadRequestException(ApplicationException):
    code: str = "BAD_REQUEST"
    status: int = 400

    @property
    def message(self) -> str:
        return 'Bad request'


@dataclass(kw_only=True)
class UnauthorizedException(ApplicationException):
    code: str = "UNAUTHORIZED"
    status: int = 401

    @property
    def message(self) -> str:
        return 'Unauthorized'


@dataclass(kw_only=True)
class ForbiddenException(ApplicationException):
    code: str = "FORBIDDEN"
    status: int = 403

    @property
    def message(self) -> str:
        return 'Forbidden'


@dataclass(kw_only=True)
class NotFoundException(ApplicationException):
    code: str = "NOT_FOUND"
    status: int = 404

    @property
    def message(self) -> str:
        return 'Not found'


@dataclass(kw_only=True)
class ConflictException(ApplicationException):
    code: str = "CONFLICT"
    status: int = 409

    @property
    def message(self) -> str:
        return 'Conflict'


@dataclass(kw_only=True)
class InvalidTokenException(ApplicationException):
    token: str
    code: str = "INVALID_TOKEN"
    status: int = 401

    @property
    def message(self) -> str:
        return 'Invalid token'


@dataclass(kw_only=True)
class PaymentException(ApplicationException):
    code: str = "PAYMENT_ERROR"
    status: int = 502

    @property
    def message(self) -> str:
        return 'Payment service error'


@dataclass(kw_only=True)
class ApiClientException(ApplicationException):
    detail: dict | None = None
    code: str = "API_CLIENT_ERROR"
    status: int = 502

    @property
    def message(self) -> str:
        return 'Remote API client error'


@dataclass(kw_only=True)
class ImageNotFoundException(ApplicationException):
    photo_key: str
    code: str = "IMAGE_NOT_FOUND"
    status: int = 500

    @property
    def message(self) -> str:
        return f'Image {self.photo_key} not found'

