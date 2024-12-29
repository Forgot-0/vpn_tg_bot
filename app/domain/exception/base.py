from dataclasses import dataclass



@dataclass(eq=False)
class ApplicationException(Exception):

    @property
    def message(self):
        return 'App error'


@dataclass(eq=False)
class TitleLong(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Very long title {len(self.text)}'


@dataclass(eq=False)
class NotValidMark(ApplicationException):
    mark: str

    @property
    def message(self):
        return f'NotValidMark {self.mark}'


@dataclass(eq=False)
class TextLong(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Very long Text {len(self.text)}'


@dataclass(eq=False)
class Empty(ApplicationException):
    @property
    def message(self):
        return 'Empty'


@dataclass(eq=False)
class SlugOnlyAscii(ApplicationException):
    @property
    def message(self):
        return 'Slug only ascii'


@dataclass(eq=False)
class NotValidUrl(ApplicationException):
    @property
    def message(self):
        return 'Url is not valid'


@dataclass(eq=False)
class InvalidEmailAddressException(ApplicationException):
    @property
    def message(self):
        return 'InvalidEmailAddressException'


@dataclass(eq=False)
class AlreadyDeletedException(ApplicationException):
    @property
    def message(self):
        return 'AlreadyDeletedException'


@dataclass(eq=False)
class NotFoundRewardsException(ApplicationException):
    @property
    def message(self):
        return 'У вас нет подарков'

