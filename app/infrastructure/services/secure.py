from dataclasses import dataclass

from cryptography.fernet import Fernet

from app.application.services.secure import SecureService



@dataclass
class FernetSecureService(SecureService):
    service: Fernet

    def encrypt(self, value: str) -> str:
        return self.service.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.service.decrypt(value).decode()