from dataclasses import dataclass

from app.domain.exception.base import ApplicationException




@dataclass(eq=False)
class LogicException(ApplicationException):
    @property
    def messege(self):
        return 'Logic exception'


@dataclass(eq=False)
class HandlersNotRegisteredExeption(LogicException):
    _type: type

    @property
    def message(self):
        return f'HandlersNotRegisteredExeption {self._type}'


@dataclass(eq=False)
class AlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'AlreadyExistsException {self.title}'


@dataclass(eq=False)
class EmailAlreadyExistsException(LogicException):
    email: str

    @property
    def message(self):
        return f'EmailAlreadyExistsException {self.email}'


@dataclass(eq=False)
class IsDeleted(LogicException):
    value: str

    @property
    def message(self):
        return f'IsDeleted {self.value}'


@dataclass(eq=False)
class NotFoundException(LogicException):
    name: str

    @property
    def message(self):
        return f'NotFoundException {self.name}'


@dataclass(eq=False)
class LimitResendActivationEmail(LogicException):
    name: str

    @property
    def message(self):
        return f'LimitResendActivationEmail {self.name}'


@dataclass(eq=False)
class LimitExceeded(LogicException):
    name: str

    @property
    def message(self):
        return f'LimitExceeded {self.name}'


@dataclass(eq=False)
class WrongException(LogicException):
    name: str

    @property
    def message(self):
        return f'WrongException {self.name}'


@dataclass(eq=False)
class NotFoundActiveSubscriptionException(LogicException):

    @property
    def message(self):
        return f'У вас нет активных подписок'
