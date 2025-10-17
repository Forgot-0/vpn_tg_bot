from dataclasses import dataclass

from cryptography.fernet import Fernet


@dataclass
class SecureService:
    service: Fernet

    def encrypt(self, value: str) -> str:
        return self.service.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.service.decrypt(value).decode()