from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SecureService(ABC):

    @abstractmethod
    def encrypt(self, value: str) -> str: ...

    @abstractmethod
    def decrypt(self, value: str) -> str: ...
