from cryptography.fernet import Fernet

from configs.app import app_settings


f = Fernet(app_settings.SECRET)

def encrypt(value: str) -> str:
    return f.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return f.decrypt(value).decode()