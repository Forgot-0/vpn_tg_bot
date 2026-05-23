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

