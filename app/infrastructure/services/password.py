from dataclasses import dataclass

from passlib.context import CryptContext

from app.application.interfaces.password import PasswordService


@dataclass
class IPasswordService(PasswordService):
    pwd_context: CryptContext

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
