from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass
class PasswordService(Protocol):
    def hash_password(self, password: str) -> str:
        ...

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...
