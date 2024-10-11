from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
from dataclasses import dataclass
import re

from domain.exception.base import (
    Empty,
    InvalidEmailAddressException,
    NotValidMark,
    NotValidUrl,
    SlugOnlyAscii,
    TextLong,
    TitleLong
)


VT = TypeVar('VT', bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[VT]):
    value: VT

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self)  -> None:
        ...

    @abstractmethod
    def as_generic_type(self):
        ...


@dataclass(frozen=True)
class Mark(BaseValueObject):
    value: int

    def validate(self):
        if self.value < 1 or self.value > 10:
            raise NotValidMark(self.value)

    def as_generic_type(self) -> int:
        return self.value


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise Empty()

        if len(self.value) > 255:
            raise TitleLong(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Name(BaseValueObject):
    value: str | None

    def validate(self):
        if self.value is None:
            return

        if not self.value:
            raise Empty()

        if len(self.value) > 255:
            raise TitleLong(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > 1024:
            raise TextLong(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)



@dataclass(frozen=True)
class Slug(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > 255:
            raise TextLong(self.value)

        if not bool(re.match(r'^[a-zA-Z0-9]+$', self.value)):
            raise SlugOnlyAscii()

        if not self.value:
            raise Empty()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Url(BaseValueObject):
    value: str

    def validate(self):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        if not bool(re.match(regex, self.value)):
            raise NotValidUrl()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject):
    value: str

    def validate(self):
        if not bool(
                re.match(
                    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
                    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
                    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', 
                    self.value, re.IGNORECASE
                )
            ): raise InvalidEmailAddressException()

    def as_generic_type(self) -> str:
        return str(self.value)


